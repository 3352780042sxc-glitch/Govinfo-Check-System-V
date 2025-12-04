import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# 获取百度新闻搜索结果的HTML，用于分析结构
def get_baidu_news_html(keyword):
    encoded_keyword = quote(keyword)
    url = f"https://www.baidu.com/s?wd={encoded_keyword}&rsv_spt=1&rsv_iqid=0xc9bcdfe301ed3bff&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&rsv_sug3=6&rsv_sug1=4&rsv_sug7=100&rsv_btype=i&prefixsug={encoded_keyword}&rsp=0&rsv_sug4=3575"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.baidu.com",
        "Upgrade-Insecure-Requests": "1"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"获取HTML失败: {e}")
        return None

# 保存HTML到文件
def save_html_to_file(html, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

# 分析HTML结构，查找摘要信息的位置
def analyze_html_structure(html):
    soup = BeautifulSoup(html, 'lxml')
    result_divs = soup.find_all('div', class_='result')
    
    print(f"找到 {len(result_divs)} 个结果")
    
    # 分析前3个结果的结构
    for i, div in enumerate(result_divs[:3], 1):
        print(f"\n=== 第 {i} 个结果的HTML结构 ===")
        print(div.prettify())

if __name__ == "__main__":
    keyword = "南昌"
    html = get_baidu_news_html(keyword)
    if html:
        # 保存HTML到文件，便于详细查看
        save_html_to_file(html, "baidu_news_structure.html")
        print("HTML已保存到 baidu_news_structure.html")
        
        # 分析HTML结构
        analyze_html_structure(html)