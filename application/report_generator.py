"""
application/report_generator.py

Report Generator.

Nhiệm vụ:
- Tạo báo cáo theo gói dịch vụ.
- Quản lý cấu hình báo cáo.
- Điều phối CustomerProfile + ReportService.

Không trực tiếp luận đoán.
"""

from __future__ import annotations



class ReportGenerator:
    """
    Bộ tạo báo cáo Bát Tự.
    """


    name = "ReportGenerator"



    REPORT_PLANS = {


        "BASIC": {

            "name":
                "Báo cáo cơ bản",


            "sections": [

                "summary",

                "day_master",

                "five_elements",

                "useful_god"

            ],


            "description":

                "Phân tích nền tảng mệnh cục."

        },



        "STANDARD": {

            "name":
                "Báo cáo tiêu chuẩn",


            "sections": [

                "summary",

                "day_master",

                "five_elements",

                "ten_gods",

                "useful_god",

                "career",

                "wealth",

                "marriage",

                "health"

            ],


            "description":

                "Phân tích toàn diện các lĩnh vực chính."

        },



        "MASTER": {

            "name":
                "Báo cáo chuyên sâu Master",


            "sections": [

                "summary",

                "day_master",

                "five_elements",

                "ten_gods",

                "useful_god",

                "combination",

                "shensha",

                "career",

                "wealth",

                "marriage",

                "children",

                "health",

                "luck",

                "fengshui"

            ],


            "description":

                "Báo cáo chuyên sâu dành cho tư vấn Master."

        }

    }




    def __init__(
        self,
        report_service
    ):


        self.report_service = (
            report_service
        )




    def generate(
        self,
        customer,
        plan="STANDARD",
        output_dir="reports"
    ):
        """
        Tạo báo cáo theo gói.
        """


        if plan not in self.REPORT_PLANS:


            raise ValueError(

                f"Không tồn tại gói báo cáo: {plan}"

            )



        config = self.REPORT_PLANS[plan]



        birth_data = (
            customer.birth_data
        )



        person_info = (

            customer.to_report_input()

        )



        report_result = (

            self.report_service.generate_report(

                birth_data,

                person_info,

                output_dir

            )

        )



        return {


            "customer":

                customer.customer_id,


            "plan":

                plan,


            "plan_name":

                config["name"],


            "sections":

                config["sections"],


            "files":

                report_result

        }




    def get_plan(
        self,
        plan_code
    ):
        """
        Lấy thông tin gói báo cáo.
        """


        return self.REPORT_PLANS.get(
            plan_code
        )




    def list_plans(
        self
    ):
        """
        Danh sách các gói.
        """


        return self.REPORT_PLANS
