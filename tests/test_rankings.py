from analysis.rankings import compute_rankings

def test_compute_rankings():
    mock_industry_analysis = {
        "Semiconductors": {
            "industry_name": "Semiconductors",
            "percentage_return_6m": 25.0,
            "companies": [
                {"symbol": "NVDA", "name": "NVIDIA", "percentage_return_6m": 40.0},
                {"symbol": "AMD", "name": "AMD", "percentage_return_6m": 10.0}
            ]
        },
        "Airlines": {
            "industry_name": "Airlines",
            "percentage_return_6m": -15.0,
            "companies": [
                {"symbol": "DAL", "name": "Delta", "percentage_return_6m": -10.0},
                {"symbol": "AAL", "name": "American", "percentage_return_6m": -20.0}
            ]
        }
    }

    rankings = compute_rankings(mock_industry_analysis)
    assert rankings["top_gainer_industry"]["industry_name"] == "Semiconductors"
    assert rankings["top_loser_industry"]["industry_name"] == "Airlines"
    assert rankings["top_gainer_company"]["symbol"] == "NVDA"
    assert rankings["top_loser_company"]["symbol"] == "AAL"
