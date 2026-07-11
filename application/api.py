"""
application/api.py

API Interface.

Nhiệm vụ:
- Nhận request tạo báo cáo.
- Điều phối ReportGenerator.
- Trả kết quả.

Không tính toán Bát Tự.
"""


from __future__ import annotations



class BaziAPI:
    """
    API Gateway cho hệ thống Bát Tự.
    """


    name = "BaziAPI"



    def __init__(
        self,
        report_generator
    ):

        self.report_generator = (
            report_generator
        )



    def create_report(
        self,
        request: dict
    ) -> dict:
        """
        Tạo báo cáo từ request.

        Input:

        {
            customer:{
                id,
                name,
                gender
            },

            birth_data:{
                year,
                month,
                day,
                hour
            },

            plan:"MASTER"
        }

        """


        customer = (
            request.get(
                "customer",
                {}
            )
        )


        birth_data = (
            request.get(
                "birth_data",
                {}
            )
        )


        plan = (

            request.get(
                "plan",
                "STANDARD"
            )

        )



        # Tạo Customer Profile

        from .customer_profile import CustomerProfile



        profile = CustomerProfile(

            customer_id=

                customer.get(
                    "id",
                    "UNKNOWN"
                ),


            name=

                customer.get(
                    "name",
                    ""
                ),


            gender=

                customer.get(
                    "gender",
                    ""
                )

        )



        profile.set_birth_data(

            birth_data

        )



        # Sinh báo cáo


        result = (

            self.report_generator.generate(

                profile,

                plan

            )

        )



        return {


            "status":

                "success",


            "engine":

                self.name,


            "data":

                result

        }




    def get_available_plans(
        self
    ) -> dict:
        """
        Lấy danh sách gói dịch vụ.
        """


        return (

            self.report_generator
            .list_plans()

        )



    def health_check(
        self
    ) -> dict:
        """
        Kiểm tra hệ thống.
        """


        return {


            "status":
                "running",


            "service":
                self.name

        }
