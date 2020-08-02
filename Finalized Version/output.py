
"""
This creates a output format and file to write the output
"""
import pandas as pd


class Output:

    header = ['Student Health Centre', 'Found by algorithm', 'Terms found', '#of Clicks', 'Path',
              'URL of page mention was found on',
              'Whether womens/birth control related section present on SHC',
              'Womens Health/Contraception Related Sections', 'Womens Health/Contraception Related Section Links',
              'Text from page that had mention']
    output_file_name = "Output18.csv"

    @classmethod
    def create_df(cls):
        df = pd.DataFrame(columns=Output.header)
        return df


    def write_to_file(df, num, fields_to_write):
        df.loc[num] = fields_to_write
        print(df.loc[num])
        df.to_csv(Output.output_file_name)
