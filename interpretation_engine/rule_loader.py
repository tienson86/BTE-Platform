import csv
import os


class RuleLoader:

    def __init__(self):
        self.rules = []


    def load_csv(self, file_path):

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Không tìm thấy file: {file_path}"
            )


        data = []

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            reader = csv.DictReader(f)

            for row in reader:

                data.append(
                    self.normalize(row)
                )


        self.rules = data

        return data



    def normalize(self,row):

        result={}

        for key,value in row.items():

            if value is None:
                value=""

            result[key.strip()] = value.strip()


        return result



    def load_folder(self,folder):

        all_rules=[]


        for file in os.listdir(folder):

            if file.endswith(".csv"):

                path=os.path.join(
                    folder,
                    file
                )

                rules=self.load_csv(path)

                all_rules.extend(rules)


        return all_rules
