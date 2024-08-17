import json
import pandas as pd
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models
from tqdm import tqdm
import time


def delay(seconds):
    time.sleep(seconds)


cred = credential.Credential("AKIDIe9gGhtVCnNtaH4rxT2qX2RvcCYidLuV", "nU5znT3fAY7VWkt5ELI4V3bhV4bwDHHE")
httpProfile = HttpProfile()
httpProfile.endpoint = "tmt.tencentcloudapi.com"

clientProfile = ClientProfile()
clientProfile.httpProfile = httpProfile
client = tmt_client.TmtClient(cred, "ap-beijing", clientProfile)


def Post_translation_data_set(row):
    try:
        req = models.TextTranslateRequest()
        req.SourceText = row['GPT-3.5生成内容']
        req.Source = 'zh'
        req.Target = 'en'
        req.ProjectId = 0
        resp = client.TextTranslate(req)
        data = json.loads(resp.to_json_string())
        row['翻译'] = data['TargetText']
        delay(0.1)
        return row
    except TencentCloudSDKException as err:
        print(err)


def read_xlsx(file_path):
    return pd.read_excel(file_path, skiprows=range(1, 3001), nrows=7000)

def save_xlsx(df, file_path):
    df.to_excel(file_path, index=False)
df = read_xlsx('10000-50000条数据集.xlsx')

# Adding progress bar
tqdm.pandas(desc="Translating...")

# Loop over dataframe with stepsize 500
for i in range(0, df.shape[0], 500):
    df[i:i + 500] = df[i:i + 500].progress_apply(Post_translation_data_set, axis=1)

    # Save every 500 rows to a new file
    save_xlsx(df[i:i + 500], f'ceshi_{i // 500}.xlsx')



