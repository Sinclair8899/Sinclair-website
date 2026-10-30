#!/usr/bin/env python3
"""Offline, socket-disabled EOD regression tests. Run this file directly."""
import contextlib
import copy
import io
import json
import math
from pathlib import Path
import socket
import tempfile
import unittest
from datetime import datetime, timezone
from unittest import mock

import update_market_brief as m


def ts(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).timestamp()


def fixture(days=None, *, zone='America/New_York', opening='13:30', closing='20:00'):
    days = days or ['2026-10-21', '2026-10-22', '2026-10-23', '2026-10-26',
                    '2026-10-27', '2026-10-28', '2026-10-29', '2026-10-30']
    periods = [[{'start': ts(d+'T'+opening+':00Z'), 'end': ts(d+'T'+closing+':00Z')}] for d in days]
    daily = {'meta': {'symbol': 'TEST', 'exchangeTimezoneName': zone, 'dataGranularity': '1d'},
             'timestamp': [p[0]['start'] for p in periods],
             'indicators': {'quote': [{'close': [100+i for i in range(len(days))],
                                       'high': [102+i for i in range(len(days))],
                                       'low': [98+i for i in range(len(days))]}]}}
    schedule = {'meta': {'symbol': 'TEST', 'exchangeTimezoneName': zone, 'tradingPeriods': periods}}
    return daily, schedule


def quote(daily):
    return daily['indicators']['quote'][0]


def select(daily, schedule, now='2026-10-30T14:00:00Z'):
    return m.completed_series(daily, schedule, ts(now))


class CompletedSessionTests(unittest.TestCase):
    def setUp(self):
        self.daily, self.schedule = fixture()

    def test_during_session_filters_all_arrays_and_metrics(self):
        quote(self.daily)['close'][-1] = 99999
        quote(self.daily)['high'][-1] = 999999
        quote(self.daily)['low'][-1] = 1
        series = select(self.daily, self.schedule)
        self.assertEqual(series.closes, list(range(100, 107)))
        self.assertEqual((series.highs[-1], series.lows[-1]), (108, 104))
        self.assertEqual(series.dates[-1], '2026-10-29')
        self.assertEqual(m.move(series.closes)['last'], 106)
        self.assertEqual(m.move(series.closes)['d1'], .95)
        self.assertEqual(m.move(series.closes)['spark'][-1], 106)
        self.assertEqual(series.provenance()['session_end_utc'], '2026-10-29T20:00:00Z')

    def test_before_open(self):
        self.daily['timestamp'].pop()
        for values in quote(self.daily).values(): values.pop()
        self.assertEqual(select(self.daily, self.schedule, '2026-10-30T12:00:00Z').dates[-1], '2026-10-29')

    def test_after_close_but_before_delivery_buffer(self):
        self.assertEqual(select(self.daily, self.schedule, '2026-10-30T20:29:59Z').dates[-1], '2026-10-29')

    def test_at_and_after_buffer(self):
        for now in ('2026-10-30T20:30:00Z', '2026-10-30T23:00:00Z'):
            with self.subTest(now=now):
                self.assertEqual(select(self.daily, self.schedule, now).dates[-1], '2026-10-30')

    def test_local_midnight_daily_label_waits_for_close(self):
        self.daily['timestamp'][-1] = ts('2026-10-30T04:00:00Z')
        self.assertEqual(select(self.daily, self.schedule).dates[-1], '2026-10-29')
        self.assertEqual(select(self.daily, self.schedule, '2026-10-30T20:30:00Z').dates[-1], '2026-10-30')

    def test_uncompleted_null_ignored(self):
        quote(self.daily)['close'][-1] = None
        self.assertEqual(select(self.daily, self.schedule).dates[-1], '2026-10-29')

    def test_completed_historical_null_preserved_not_compacted(self):
        quote(self.daily)['close'][-2] = None
        # Current day complete, prior day unknown: price is dated/valid but 1D
        # and 1W are unavailable, not computed against two sessions ago.
        series = select(self.daily, self.schedule, '2026-10-30T21:00:00Z')
        self.assertEqual(len(series.closes), 8)
        self.assertIsNone(series.closes[-2])
        self.assertIsNone(m.move(series.closes)['d1'])
        self.assertIsNone(m.move(series.closes)['w1'])
        self.assertIsNone(m.move(series.closes)['spark'][-2])
        self.assertIsNone(m.macro_row('X', 'X', 'price', series.closes)['d1'])

    def test_missing_timestamp_session_fails(self):
        self.daily['timestamp'].pop(-2)
        for values in quote(self.daily).values(): values.pop(-2)
        with self.assertRaisesRegex(ValueError, 'no recent verified'): select(self.daily, self.schedule)

    def test_missing_older_timestamp_preserved_as_unknown_session(self):
        self.daily['timestamp'].pop(-3)
        for values in quote(self.daily).values(): values.pop(-3)
        series = select(self.daily, self.schedule)
        self.assertEqual(series.dates[-2], '2026-10-28')
        self.assertIsNone(series.closes[-2])
        self.assertIsNone(m.move(series.closes)['d1'])

    def test_missing_latest_completed_close_fails(self):
        quote(self.daily)['close'][-1] = None
        with self.assertRaisesRegex(ValueError, 'no recent verified'):
            select(self.daily, self.schedule, '2026-10-30T21:00:00Z')

    def test_missing_range_is_not_another_bars_range(self):
        quote(self.daily)['high'] = [102]
        quote(self.daily).pop('low')
        s = select(self.daily, self.schedule)
        self.assertIsNone(s.highs[-1]); self.assertIsNone(s.lows[-1])

    def test_invalid_close_fails(self):
        for bad in (float('nan'), float('inf'), 0, -1, '106', True):
            with self.subTest(bad=bad):
                daily = copy.deepcopy(self.daily); quote(daily)['close'][-2] = bad
                with self.assertRaises(ValueError): select(daily, self.schedule)

    def test_invalid_range_fails(self):
        quote(self.daily)['high'][-2] = float('nan')
        with self.assertRaisesRegex(ValueError, 'session range'): select(self.daily, self.schedule)

    def test_future_bar_fails(self):
        with self.assertRaisesRegex(ValueError, 'future daily bar'):
            select(self.daily, self.schedule, '2026-10-30T12:00:00Z')

    def test_all_null_explicit_future_session_placeholder_ignored(self):
        for values in quote(self.daily).values(): values[-1] = None
        self.assertEqual(select(self.daily, self.schedule, '2026-10-30T12:00:00Z').dates[-1], '2026-10-29')
        self.schedule['meta']['tradingPeriods'].pop()
        with self.assertRaisesRegex(ValueError, 'future daily bar'):
            select(self.daily, self.schedule, '2026-10-30T12:00:00Z')

    def test_alignment_fails(self):
        quote(self.daily)['close'].pop()
        with self.assertRaisesRegex(ValueError, 'unaligned'): select(self.daily, self.schedule)

    def test_duplicate_and_unsorted_timestamps_fail(self):
        for bad in (self.daily['timestamp'][-2], self.daily['timestamp'][0]-1):
            daily = copy.deepcopy(self.daily); daily['timestamp'][-1] = bad
            with self.assertRaisesRegex(ValueError, 'timestamps'): select(daily, self.schedule)

    def test_invalid_timestamp_fails(self):
        for bad in (None, 'date', float('nan'), True, 0):
            daily = copy.deepcopy(self.daily); daily['timestamp'][-1] = bad
            with self.assertRaises(ValueError): select(daily, self.schedule)

    def test_missing_metadata_fails(self):
        for key in ('tradingPeriods', 'exchangeTimezoneName', 'symbol'):
            schedule = copy.deepcopy(self.schedule); del schedule['meta'][key]
            with self.assertRaises(KeyError): select(self.daily, schedule)

    def test_symbol_and_timezone_mismatch_fail(self):
        for key, bad in (('symbol', 'OTHER'), ('exchangeTimezoneName', 'Europe/London')):
            schedule = copy.deepcopy(self.schedule); schedule['meta'][key] = bad
            with self.assertRaises(ValueError): select(self.daily, schedule)

    def test_unknown_zone_fails(self):
        self.daily['meta']['exchangeTimezoneName'] = 'Not/A_Zone'
        with self.assertRaises(KeyError): select(self.daily, self.schedule)

    def test_non_daily_fails(self):
        self.daily['meta']['dataGranularity'] = '1h'
        with self.assertRaisesRegex(ValueError, 'not daily'): select(self.daily, self.schedule)

    def test_pre_and_post_not_used(self):
        periods = self.schedule['meta']['tradingPeriods']
        self.schedule['meta']['tradingPeriods'] = {'regular': periods, 'pre': [[{'start': 1, 'end': 2}]], 'post': []}
        self.assertEqual(select(self.daily, self.schedule).dates[-1], '2026-10-29')

    def test_weekend_without_guessing_a_calendar(self):
        self.assertEqual(select(self.daily, self.schedule, '2026-11-01T12:00:00Z').dates[-1], '2026-10-30')

    def test_explicit_early_close(self):
        self.schedule['meta']['tradingPeriods'][-1][0]['end'] = ts('2026-10-30T17:00:00Z')
        self.assertEqual(select(self.daily, self.schedule, '2026-10-30T17:30:00Z').dates[-1], '2026-10-30')

    def test_dst_offsets_come_from_each_period(self):
        daily, schedule = fixture(['2026-03-05', '2026-03-06', '2026-03-09'])
        for i in (0, 1):
            daily['timestamp'][i] += 3600
            schedule['meta']['tradingPeriods'][i][0]['start'] += 3600
            schedule['meta']['tradingPeriods'][i][0]['end'] += 3600
        before = select(daily, schedule, '2026-03-09T19:59:00Z')
        self.assertEqual(before.provenance()['session_end_utc'], '2026-03-06T21:00:00Z')
        after = select(daily, schedule, '2026-03-09T20:30:00Z')
        self.assertEqual(after.provenance()['session_end_utc'], '2026-03-09T20:00:00Z')

    def test_overnight_session_after_utc_midnight_is_not_complete(self):
        daily, schedule = fixture(['2026-10-28', '2026-10-29', '2026-10-30'], zone='Europe/London', opening='22:00', closing='23:00')
        for p in schedule['meta']['tradingPeriods']: p[0]['end'] += 23*3600
        self.assertEqual(select(daily, schedule, '2026-10-31T01:00:00Z').dates[-1], '2026-10-29')
        self.assertEqual(select(daily, schedule, '2026-10-31T22:30:00Z').dates[-1], '2026-10-30')

    def test_ambiguous_midnight_between_overnight_sessions_fails(self):
        daily, schedule = fixture(['2026-10-28', '2026-10-29', '2026-10-30'], zone='Europe/London', opening='22:00', closing='23:00')
        for p in schedule['meta']['tradingPeriods']: p[0]['end'] += 21*3600
        daily['timestamp'][-1] = ts('2026-10-30T00:00:00Z')
        with self.assertRaisesRegex(ValueError, 'ambiguous daily bar'):
            select(daily, schedule, '2026-10-30T21:00:00Z')

    def test_invalid_cutoff_fails(self):
        with self.assertRaisesRegex(ValueError, 'invalid observation cutoff'):
            m.completed_series(self.daily, self.schedule, float('nan'))

    def test_fx_day_and_futures_day(self):
        for zone, opening, closing, now in [('Europe/London', '00:00', '23:59', '2026-10-30T21:30:00Z'),
                                            ('America/New_York', '04:00', '03:59', '2026-10-30T21:30:00Z')]:
            daily, schedule = fixture(zone=zone, opening=opening, closing=closing)
            if closing < opening:
                for p in schedule['meta']['tradingPeriods']: p[0]['end'] += 86400
            self.assertEqual(select(daily, schedule, now).dates[-1], '2026-10-29')

    def test_unknown_recent_bar_fails(self):
        self.schedule['meta']['tradingPeriods'].pop(-2)
        with self.assertRaisesRegex(ValueError, 'coverage'): select(self.daily, self.schedule)

    def test_overlapping_or_invalid_period_fails(self):
        for end in (0, float('nan'), self.schedule['meta']['tradingPeriods'][-1][0]['end']+86400):
            schedule = copy.deepcopy(self.schedule); schedule['meta']['tradingPeriods'][-2][0]['end'] = end
            with self.assertRaises(ValueError): select(self.daily, schedule)

    def test_old_history_retained_but_never_as_latest_price(self):
        self.schedule['meta']['tradingPeriods'] = self.schedule['meta']['tradingPeriods'][-3:]
        s = select(self.daily, self.schedule)
        self.assertEqual(s.closes[0], 100)
        self.daily['timestamp'] = self.daily['timestamp'][:4]
        for key in quote(self.daily): quote(self.daily)[key] = quote(self.daily)[key][:4]
        with self.assertRaisesRegex(ValueError, 'no recent'): select(self.daily, self.schedule)

    def test_null_no_session_placeholder_excluded_by_provider_evidence(self):
        self.schedule['meta']['tradingPeriods'].pop(2)
        for key in quote(self.daily): quote(self.daily)[key][2] = None
        result = select(self.daily, self.schedule)
        self.assertNotIn('2026-10-23', result.dates)
        self.assertEqual(len(result.closes), 6)

    def test_partial_no_session_placeholder_fails(self):
        self.schedule['meta']['tradingPeriods'].pop(2)
        quote(self.daily)['close'][2] = None
        with self.assertRaisesRegex(ValueError, 'coverage'): select(self.daily, self.schedule)

    def test_nullable_metric_windows(self):
        closes = list(range(1, 261))
        closes[-10] = None
        self.assertIsNotNone(m.move(closes)['w1'])
        for key, value in m.moving_averages(closes).items(): self.assertIsNone(value, key)
        self.assertIsNone(m.drawdown_52w(closes))
        closes[-10] = 251
        self.assertIsNotNone(m.drawdown_52w(closes))
        self.assertIsNone(m.drawdown_52w(closes[:100]))

    def test_window_hole_prevents_week_return_despite_valid_endpoints(self):
        closes = [100, 101, None, 103, 104, 105]
        self.assertIsNotNone(m.move(closes)['d1'])
        self.assertIsNone(m.move(closes)['w1'])
        for kind in ('price', 'yield', 'points'):
            self.assertIsNone(m.macro_row('X', 'X', kind, closes)['w1'])


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root/'assets').mkdir()
        self.path = self.root/'assets/market_brief.json'
        self.path.write_text('previous dated brief\n')
        self.daily, self.schedule = fixture()
        self.series = select(self.daily, self.schedule)
        spec = dict(m.BASKETS[0], members=[('US', 'US member'), ('KR', 'Korean member')])
        self.stack = contextlib.ExitStack()
        self.stack.enter_context(mock.patch.object(m, 'INDICES', [('INDEX', 'Test', 'IDX')]))
        self.stack.enter_context(mock.patch.object(m, 'MACRO', [('MACRO', 'Macro', 'FX', 'price')]))
        self.stack.enter_context(mock.patch.object(m, 'BASKETS', [spec]))
        self.stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
        self.stack.enter_context(contextlib.redirect_stderr(io.StringIO()))

    def tearDown(self):
        self.stack.close(); self.temp.cleanup()

    def run_main(self, fetch):
        with mock.patch.object(m, 'fetch_series', side_effect=fetch):
            return m.main(str(self.root), ts('2026-10-30T21:00:00Z'))

    def test_one_failure_preserves_old_bytes(self):
        self.assertEqual(self.run_main(lambda symbol, **_: None if symbol == 'KR' else self.series), 1)
        self.assertEqual(self.path.read_text(), 'previous dated brief\n')
        self.assertFalse(Path(str(self.path)+'.tmp').exists())

    def test_all_unavailable_preserves_old_bytes(self):
        self.assertEqual(self.run_main(lambda *a, **kw: None), 1)
        self.assertEqual(self.path.read_text(), 'previous dated brief\n')

    def test_basket_common_date_and_filtered_provenance(self):
        later = select(self.daily, self.schedule, '2026-10-30T21:00:00Z')
        self.assertEqual(self.run_main(lambda symbol, **_: later if symbol == 'KR' else self.series), 0)
        data = json.loads(self.path.read_text())
        basket = data['baskets'][0]
        self.assertEqual(basket['source_date'], '2026-10-29')
        self.assertEqual(basket['d1_start_date'], '2026-10-28')
        self.assertEqual(basket['w1_start_date'], '2026-10-22')
        self.assertEqual({mm['source_date'] for mm in basket['members']}, {'2026-10-29'})
        self.assertEqual(basket['d1'], .95)
        self.assertEqual(data['source_date_max'], '2026-10-29')
        self.assertEqual(data['indices'][0]['spark'][-1], 106)
        self.assertEqual(data['indices'][0]['day_high'], 108)
        self.assertEqual(data['macro'][0]['value'], '106.00')
        self.assertTrue(any('歷史' in w for w in data['summary']['warnings']))

    def test_nullable_basket_metrics_do_not_drop_members_or_reweight(self):
        with_hole = copy.deepcopy(self.series)
        with_hole.closes[-2] = None
        self.assertEqual(self.run_main(lambda symbol, **_: with_hole if symbol == 'KR' else self.series), 0)
        data = json.loads(self.path.read_text()); b = data['baskets'][0]
        self.assertEqual(b['count'], 2)
        self.assertEqual(b['return_covered'], 1)
        self.assertIsNone(b['d1']); self.assertIsNone(b['w1'])
        self.assertEqual(b['dd52_covered'], 0)
        self.assertEqual(data['fcn']['tracked'], 2)
        self.assertEqual(data['fcn']['assessed'], 0)

    def test_atomic_replace_failure_preserves_old_bytes(self):
        with mock.patch.object(m.os, 'replace', side_effect=OSError('injected')):
            with self.assertRaises(OSError): self.run_main(lambda *a, **kw: self.series)
        self.assertEqual(self.path.read_text(), 'previous dated brief\n')
        self.assertFalse(Path(str(self.path)+'.tmp').exists())

    def test_fetch_uses_fixed_clock_and_both_payloads(self):
        payloads = [io.BytesIO(json.dumps({'chart': {'result': [r]}}).encode()) for r in (self.daily, self.schedule)]
        with mock.patch.object(m.urllib.request, 'urlopen', side_effect=payloads) as fetch:
            result = m.fetch_series('TEST', retries=1, now=ts('2026-10-30T14:00:00Z'))
        self.assertEqual(result.dates[-1], '2026-10-29')
        self.assertIn('range=1mo&interval=1h', fetch.call_args_list[1].args[0].full_url)

    def test_fetch_wrong_symbol_fails_closed(self):
        payloads = [io.BytesIO(json.dumps({'chart': {'result': [r]}}).encode()) for r in (self.daily, self.schedule)]
        with mock.patch.object(m.urllib.request, 'urlopen', side_effect=payloads):
            self.assertIsNone(m.fetch_series('OTHER', retries=1, now=ts('2026-10-30T14:00:00Z')))

    def test_retry_exhaustion_returns_failure(self):
        with mock.patch.object(m.urllib.request, 'urlopen', side_effect=OSError('offline')), mock.patch.object(m.time, 'sleep'):
            self.assertIsNone(m.fetch_series('TEST', retries=2))


class NarrativeTests(unittest.TestCase):
    def baskets(self):
        return [dict(key='ai_infra', zh_short='AI', d1=2, source_date='2026-10-29', d1_start_date='2026-10-28'),
                dict(key='semis_hbm', zh_short='Semis', d1=1, source_date='2026-10-29', d1_start_date='2026-10-28')]

    def test_matching_basket_intervals_can_compare(self):
        result = m.build_summary([], self.baskets(), [])
        self.assertIsNotNone(result['lens'])
        self.assertTrue(any('漲幅最大' in f for f in result['facts']))

    def test_different_end_or_start_dates_cannot_compare(self):
        for key in ('source_date', 'd1_start_date'):
            baskets = self.baskets(); baskets[1][key] = '2026-10-27'
            result = m.build_summary([], baskets, [])
            self.assertIsNone(result['lens'])
            self.assertTrue(any('不直接比較' in f for f in result['facts']))
            self.assertFalse(any('漲幅最大' in f for f in result['facts']))

    def test_unknown_basket_does_not_become_all_baskets_claim(self):
        baskets = self.baskets() + [dict(key='unknown', zh_short='Unknown', d1=None)]
        result = m.build_summary([], baskets, [])
        self.assertTrue(any('可計算日變動的研究籃子全數收高' in f for f in result['facts']))
        self.assertFalse(any(f.startswith('研究籃子全數') for f in result['facts']))

    def test_unknown_asia_and_ma_coverage_are_explicit(self):
        indices = [dict(code='TAIEX', name='Taiwan', d1=-1, ma20_gap=-1, last=100),
                   dict(code='N225', name='Japan', d1=-1, ma20_gap=-1, last=100),
                   dict(code='KS11', name='Korea', d1=None, ma20_gap=None, last=100)]
        result = m.build_summary(indices, [], [])
        self.assertTrue(any('可計算日變動的亞洲市場全面收低' in f for f in result['facts']))
        self.assertTrue(any('有完整月線資料的 2 個指數' in f for f in result['facts']))


if __name__ == '__main__':
    with mock.patch.object(socket, 'socket', side_effect=AssertionError('network forbidden in offline tests')):
        unittest.main(verbosity=2)
