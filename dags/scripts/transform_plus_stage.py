from word2number import w2n
from snowflake.connector.pandas_tools import write_pandas
from nltk.tokenize import word_tokenize
import utils.utils



def marks_tags(df):
    tag_filters = ['sql','python','airflow','etl','snowflake','aws','azure','gcp','bigquery','spark','hadoop','hive','lambda','dbt', 'google','amazon','microsoft','bi','tableau','power','looker', 'excel','javascript','react','vue']
    for tag in tag_filters:
        df[tag]=0

    for i in range(df.shape[0]):
        paraSplitted = df.loc[i,'description'].replace(","," ").replace('+'," ").replace('/'," ").replace("'"," ").replace("-"," ").replace('('," ").replace(')'," ").lower().split()
        paraSplitted = [word.replace(","," ").replace('+'," ").replace('/'," ").replace("'"," ").replace('-','') for word in paraSplitted]
        
        # Marking tags
        for word in paraSplitted:
            for tag in tag_filters:
                if tag == word:
                    df.loc[i,tag]=1
    return df



def marks_YoE(df):
    years_to_colum = ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
    years = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15',
             'one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve',
            'thirteen','fourteen','fifteen']
    for year in years_to_colum:
        df[year]=0
    
    counter = 0
    for i in range(df.shape[0]):
        paraSplitted = df.loc[i,'description'].replace(","," ").replace('+'," ").replace('/'," ").replace("'"," ").replace("-"," ").replace('('," ").replace(')'," ").lower().split()
        paraSplitted = [word.replace(","," ").replace('+'," ").replace('/'," ").replace("'"," ").replace('-','') for word in paraSplitted]
        
        # Marking years
        expIndices = [i for i in range(len(paraSplitted)) if 'experience' == paraSplitted[i]]
        counter = counter + len(expIndices)
        for instance_of_exp in expIndices:
            count = 0
            for year in years:  
                # Marks years 1 -15
                if year in paraSplitted[instance_of_exp-10:instance_of_exp+10]:
                    # Marks single digit years, 1 - 9
                    if len(year) == 1 or len(year)==2:
                        df.loc[i,str(year)]=1
                        count += 1
                    # Marks years 10-15
                    else:
                        df.loc[i,str(w2n.word_to_num(year))]=1
                        count += 1
        # Marks jobs with no specific YoE req.
        if 1 not in [df.loc[i,str(j)] for j in range(1,16)]:
            df.loc[i,'0']=1

    return df



def remove_titles(df):
    rejectTitles = ['manager','summer','intern/co-op','co-op','coop', 'student', 'intership', 'vice president','vp','intern','senior','sr','sr.','director','principal','architect', 'lead']
    df['remove_titles']= 0

    for i in range(df.shape[0]):
        title_tokens = word_tokenize(df.title[i].replace('-',''))

        title_tokens_clean = [word.lower() for word in title_tokens]
        if (any(word in title_tokens_clean for word in rejectTitles)):
            df.loc[i,'remove_titles'] = 1

    return df



def load_to_stagingTable(df):
    con = get_snowflake_connector()

    #creates empty staging table, with every field as a string
    con.cursor().execute(f"CREATE OR REPLACE TABLE JOB_POSTINGS_STAGE (" + " ".join([str(df.columns[i]).upper() + " STRING," for i in range(len(df.columns))])[:-1] + ");" )

    success, num_chunks, num_rows, output = write_pandas(con, df, 'JOB_POSTINGS_STAGE')
    print(success,num_rows)  
    con.close()


def main(s3Bucket, s3FileName_key):
    df = load_csv_from_s3(s3Bucket, s3FileName_key)
    transformed_df = remove_titles(marks_YoE(df))
    load_to_stagingTable(transformed_df)


