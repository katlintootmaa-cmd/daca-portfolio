"""Offline regression checks for API extraction and report date boundaries."""

import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import data_fetcher
import pipeline


class PipelineTests(unittest.TestCase):
    def test_environment_uses_project_path(self):
        with patch.object(data_fetcher, "load_dotenv") as load:
            data_fetcher.load_environment()
        load.assert_called_once_with(dotenv_path=data_fetcher.PROJECT_ROOT / ".env")

    def test_invalid_pagination_options_fail_before_request(self):
        for options in ({"page_size": 0}, {"max_retries": 0}, {"retry_base_seconds": -1}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                data_fetcher.fetch_table(MagicMock(), "sales", **options)

    def test_pagination_retries_failed_page_and_includes_final_day(self):
        client = MagicMock()
        query = client.table.return_value.select.return_value
        query.lt.return_value = query
        query.range.return_value = query
        query.execute.side_effect = [
            OSError("temporary failure"),
            MagicMock(data=[{"sale_id": 1}, {"sale_id": 2}]),
            MagicMock(data=[{"sale_id": 3}]),
        ]
        result = data_fetcher.fetch_table(
            client, "sales", page_size=2, retry_base_seconds=0,
            date_column="sale_date", end_date="2025-02-28",
        )
        self.assertEqual(result["sale_id"].tolist(), [1, 2, 3])
        self.assertEqual(query.range.call_args_list[-1].args, (2, 3))
        query.lt.assert_called_with("sale_date", "2025-03-01T00:00:00")

    def test_empty_api_response_uses_fallback(self):
        fallback = data_fetcher.sample_data()
        with patch.object(pipeline, "create_supabase_client"), \
             patch.object(pipeline, "fetch_sales", return_value=pd.DataFrame()), \
             patch.object(pipeline, "fetch_customers", return_value=fallback[1]), \
             patch.object(pipeline, "fetch_products", return_value=fallback[2]), \
             patch.object(pipeline, "csv_fallback_data", return_value=fallback):
            result = pipeline.extract(pipeline.load_config())
        self.assertEqual(result[-1], "csv_fallback")

    def test_fallback_honors_both_date_boundaries(self):
        sales, customers, products = data_fetcher.sample_data()
        sales = sales.iloc[:4].copy()
        sales["sale_date"] = pd.to_datetime([
            "2025-01-31 23:59:59", "2025-02-01 00:00:00",
            "2025-02-28 23:59:59", "2025-03-01 00:00:00",
        ])
        config = pipeline.load_config()
        config["date_filter"] = {"start_date": "2025-02-01", "end_date": "2025-02-28"}
        result = pipeline.transform_data(sales, customers, products, config, "csv_fallback")
        pipeline.validate_results(result)
        self.assertEqual(result["clean_sales"]["sale_id"].tolist(), [2, 3])
        self.assertEqual(result["rfm"]["recency_days"].min(), 0)

    def test_empty_period_has_clear_error(self):
        config = pipeline.load_config()
        config["date_filter"]["start_date"] = "2030-01-01"
        with self.assertRaisesRegex(ValueError, "müügiandmeid"):
            pipeline.transform_data(*data_fetcher.sample_data(), config)


if __name__ == "__main__":
    unittest.main()
