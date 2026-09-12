from .db_repository import db_repository

class ROIService:
    def calculate_roi(self):
        query = """
        SELECT d.expected_cost, o.actual_cost, o.actual_profit 
        FROM SUPPLYPRESCRIPT_DECISIONS d
        JOIN SUPPLYPRESCRIPT_ACTUAL_OUTCOMES o ON d.decision_id = o.decision_id
        """
        results = db_repository.fetchall(query)
        
        total_expected_cost = sum(r['expected_cost'] for r in results) if results else 0
        total_actual_cost = sum(r['actual_cost'] for r in results) if results else 0
        total_profit_saved = sum(r['actual_profit'] for r in results) if results else 0
        
        # Simplified ROI: (Profit Saved - Actual Cost) / Expected Cost
        net_value = total_profit_saved - total_actual_cost
        roi_percentage = (net_value / total_expected_cost * 100) if total_expected_cost > 0 else 0
        
        return {
            "total_decisions_reconciled": len(results),
            "total_expected_cost": total_expected_cost,
            "total_actual_cost": total_actual_cost,
            "total_profit_saved": total_profit_saved,
            "net_value_generated": net_value,
            "roi_percentage": roi_percentage
        }

roi_service = ROIService()
