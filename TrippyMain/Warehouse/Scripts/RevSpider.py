from RevScraper import primary_crawler, save_reviews
import pandas as pd

udp_placelist_1 = 'https://www.tripadvisor.in/Attractions-g297672-Activities-Udaipur_Udaipur_District_Rajasthan.html'
udp_placelist_2 = 'https://www.tripadvisor.in/Attractions-g297672-Activities-oa30-Udaipur_Udaipur_District_Rajasthan.html'
udp_placelist_3 = 'https://www.tripadvisor.in/Attractions-g297672-Activities-oa60-Udaipur_Udaipur_District_Rajasthan.html'

primary_crawler(udp_placelist_1)
save_reviews('Udaipur_reviews1.pkl')

primary_crawler(udp_placelist_2)
save_reviews('Udaipur_reviews2.pkl')

primary_crawler(udp_placelist_3)
save_reviews('Udaipur_reviews3.pkl')

df1 = pd.read_pickle('Udaipur_reviews1.pkl')
df2 = pd.read_pickle('Udaipur_reviews2.pkl')
df3 = pd.read_pickle('Udaipur_reviews3.pkl')

df_all = [df1, df2, df3]
df_all = pd.concat(df_all)
df_all.to_pickle('UdpRevFin.pkl')
