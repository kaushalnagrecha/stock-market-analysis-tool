from typing import Dict, List, Any

def compute_rankings(
    industry_analysis: Dict[str, Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Computes all rankings required for KPI cards and Dashboard charts.
    """
    if not industry_analysis:
        return {}

    # Sort industries by 6-month percentage return
    sorted_industries = sorted(
        industry_analysis.values(),
        key=lambda x: x["percentage_return_6m"],
        reverse=True
    )

    top_gainer_industry = sorted_industries[0]
    top_loser_industry = sorted_industries[-1]
    top_5_gainer_industries = sorted_industries[:5]
    top_3_gainer_industries = sorted_industries[:3]

    # Collect all companies across all industries for overall company ranking
    all_companies: List[Dict[str, Any]] = []
    for ind in industry_analysis.values():
        all_companies.extend(ind.get("companies", []))

    sorted_companies = sorted(
        all_companies,
        key=lambda x: x["percentage_return_6m"],
        reverse=True
    )

    top_gainer_company = sorted_companies[0] if sorted_companies else {}
    top_loser_company = sorted_companies[-1] if sorted_companies else {}

    # Collect all companies belonging to the Top 3 Gaining Industries
    top_3_industry_names = {ind["industry_name"] for ind in top_3_gainer_industries}
    top_3_ind_companies: List[Dict[str, Any]] = []

    for ind in top_3_gainer_industries:
        for comp in ind.get("companies", []):
            comp_copy = comp.copy()
            comp_copy["industry"] = ind["industry_name"]
            top_3_ind_companies.append(comp_copy)

    sorted_top3_companies = sorted(
        top_3_ind_companies,
        key=lambda x: x["percentage_return_6m"],
        reverse=True
    )

    top_5_gaining_companies_in_top_3_ind = sorted_top3_companies[:5]
    top_5_losing_companies_in_top_3_ind = sorted_top3_companies[-5:] if len(sorted_top3_companies) >= 5 else sorted_top3_companies

    return {
        "top_gainer_industry": top_gainer_industry,
        "top_loser_industry": top_loser_industry,
        "top_gainer_company": top_gainer_company,
        "top_loser_company": top_loser_company,
        "top_5_gainer_industries": top_5_gainer_industries,
        "top_3_gainer_industries": top_3_gainer_industries,
        "top_5_gaining_companies_in_top_3_industries": top_5_gaining_companies_in_top_3_ind,
        "top_5_losing_companies_in_top_3_industries": top_5_losing_companies_in_top_3_ind
    }
