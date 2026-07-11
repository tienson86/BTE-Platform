"""
application/customer_profile.py

Customer Profile.

Quản lý hồ sơ khách hàng trong hệ thống Bát Tự.

Nhiệm vụ:
- Lưu thông tin khách hàng.
- Chuẩn hóa dữ liệu sinh.
- Theo dõi lịch sử báo cáo.

Không tính toán Bát Tự.
"""


from __future__ import annotations


from datetime import datetime



class CustomerProfile:
    """
    Hồ sơ khách hàng.
    """

    name = "CustomerProfile"



    def __init__(
        self,
        customer_id: str,
        name: str = "",
        gender: str = "",
    ):

        self.customer_id = customer_id

        self.name = name

        self.gender = gender


        self.birth_data = {}


        self.contact = {}


        self.services = []


        self.reports = []



    def set_birth_data(
        self,
        birth_data: dict
    ):
        """
        Lưu thông tin ngày giờ sinh.
        """


        self.birth_data = {

            "year":
                birth_data.get(
                    "year"
                ),


            "month":
                birth_data.get(
                    "month"
                ),


            "day":
                birth_data.get(
                    "day"
                ),


            "hour":
                birth_data.get(
                    "hour"
                ),


            "minute":
                birth_data.get(
                    "minute",
                    0
                ),


            "calendar":
                birth_data.get(
                    "calendar",
                    "solar"
                ),


            "timezone":
                birth_data.get(
                    "timezone",
                    "Asia/Ho_Chi_Minh"
                )

        }



    def update_contact(
        self,
        contact: dict
    ):
        """
        Cập nhật thông tin liên hệ.
        """


        self.contact.update(
            contact
        )



    def add_service(
        self,
        service_name: str
    ):
        """
        Thêm gói dịch vụ.
        """


        if service_name not in self.services:

            self.services.append(
                service_name
            )



    def add_report(
        self,
        report_info: dict
    ):
        """
        Lưu lịch sử báo cáo.
        """


        report_record = {


            "created_at":

                datetime.now()
                .isoformat(),


            "report":

                report_info

        }


        self.reports.append(
            report_record
        )



    def get_profile(
        self
    ) -> dict:
        """
        Xuất dữ liệu hồ sơ.
        """


        return {


            "customer_id":
                self.customer_id,


            "name":
                self.name,


            "gender":
                self.gender,


            "birth_data":
                self.birth_data,


            "contact":
                self.contact,


            "services":
                self.services,


            "reports":
                self.reports

        }



    def to_report_input(
        self
    ) -> dict:
        """
        Chuyển thành dữ liệu cho Report Service.
        """


        return {


            "name":
                self.name,


            "gender":
                self.gender,


            "birth_date":

                self.format_birth_date(),


            "birth_time":

                self.format_birth_time()

        }



    def format_birth_date(
        self
    ) -> str:


        return (

            f"{self.birth_data.get('day','')}/"

            f"{self.birth_data.get('month','')}/"

            f"{self.birth_data.get('year','')}"

        )



    def format_birth_time(
        self
    ) -> str:


        return (

            f"{self.birth_data.get('hour','')}"

            ":"

            f"{self.birth_data.get('minute',0)}"

        )
