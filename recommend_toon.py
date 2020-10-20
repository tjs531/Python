import numpy as np
import pandas as pd
import pymysql

GENRE_WEIGHT=0.1 

def pearsonR(s1, s2):
    s1_c = s1 - s1.mean()
    s2_c = s2 - s2.mean()
    if np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))!=0:  
        return np.sum(s1_c * s2_c) / np.sqrt(np.sum(s1_c ** 2) * np.sum(s2_c ** 2))

def recommend(input_toon, matrix, n, similar_genre=True):
    input_genres = result_webtoon[result_webtoon['w_no'] == input_toon]['genre_name'].iloc(0)[0].split(",")
    
    result = []
    for no in matrix.columns:

        if no == input_toon:
            continue

        cor = pearsonR(matrix[input_toon], matrix[no])

        if similar_genre and len(input_genres) > 0  and str(cor) != 'None':
            temp_genres = result_webtoon[result_webtoon['w_no'] == no]['genre_name'].iloc(0)[0].split(",")

            same_count = np.count_nonzero(np.in1d(temp_genres, input_genres, assume_unique=True)== True)

            cor += (GENRE_WEIGHT * same_count)

        if str(cor)=='None':
           continue
        else:
            result.append((no, float('{:.2f}'.format(cor))))            #float()을 이용하면 문자를 숫자로 인식해서 음수인 경우도 제대로 정렬 됨.

    result.sort(key=lambda r: r[1], reverse=True)    

    return result[:n]




connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='webtoon_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print("DB접속성공!")

try:
    with connection.cursor() as cursor:
        sql_webtoon = """select a.w_no, a.w_title, group_concat(c.genre_name separator ', ') as genre_name from t_webtoon A
                            left join t_w_genre B
                            on a.w_no = b.w_no
                            left join t_genre C
                            on b.genre_no = c.genre_no
                            group by w_no;"""
        sql_user = """SELECT * FROM `t_comment`"""
        result_webtoon = pd.read_sql(sql_webtoon,connection)
        result_rating = pd.read_sql(sql_user,connection)
        result_rating = result_rating[['u_no','w_no','c_rating']]
        result_rating.head()

        result_webtoon.w_no = pd.to_numeric(result_webtoon.w_no, errors='coerce')
        result_rating.w_no = pd.to_numeric(result_rating.w_no, errors='coerce')

        data = pd.merge(result_webtoon, result_rating, on='w_no', how='left')
        matrix = data.pivot_table(index='u_no', columns='w_no', values='c_rating')          #매트릭스에 빈 컬럼(단 한명도 평점을 주지 않았을 경우)은 포함되지 않음.

        recomment_result = recommend(w_no_args, matrix, 5, similar_genre=True)
        #recomment_result = recommend(5, matrix, 5, similar_genre=True)

        result = pd.DataFrame(recomment_result, columns=['w_no','Correlation'])

        #print(recomment_result)
        #print(result)

finally:
    connection.close()
