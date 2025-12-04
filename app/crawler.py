import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import time
import random

# 百度新闻搜索爬虫
def baidu_news_crawler(keyword, pages=3, quantity=30):
    # 编码关键字
    encoded_keyword = quote(keyword)
    
    # 设置请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.baidu.com",
        "Upgrade-Insecure-Requests": "1"
    }
    
    # 提取新闻信息
    news_results = []
    
    try:
        # 循环爬取多页
        for page in range(pages):
            # 构造百度新闻搜索URL，包含分页参数
            pn = page * 10  # 百度搜索每页10条结果，pn参数表示起始位置
            url = f"https://www.baidu.com/s?wd={encoded_keyword}&rsv_spt=1&rsv_iqid=0xc9bcdfe301ed3bff&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_dl=tb&rsv_sug3=6&rsv_sug1=4&rsv_sug7=100&rsv_btype=i&prefixsug={encoded_keyword}&rsp=0&rsv_sug4=3575&pn={pn}"
            
            # 发送请求
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # 百度新闻搜索结果通常在class为"result"的div中
            result_divs = soup.find_all('div', class_='result')
            
            # 如果没有找到结果，可能是被反爬了，退出循环
            if not result_divs:
                print(f"第{page+1}页没有找到结果，可能被反爬了")
                break
            
            for div in result_divs:
                # 提取标题
                title_elem = div.find('h3')
                if title_elem:
                    title = title_elem.text.strip()
                    
                    # 提取链接
                    link_elem = title_elem.find('a')
                    if link_elem and 'href' in link_elem.attrs:
                        link = link_elem['href']
                        
                        # 提取概要（尝试多种可能的class名）
                        summary = ""
                        # 尝试多种可能的摘要元素选择器
                        summary_elem = div.find('div', class_='c-abstract') or \
                                        div.find('div', class_='abstract') or \
                                        div.find('div', class_='content') or \
                                        div.find('div', class_='cos-line-clamp-2') or \
                                        div.find('div', class_='aladdin_7vNuJ') or \
                                        div.find('div', class_='aladdin-struct_r13eS')
                        
                        if summary_elem:
                            summary = summary_elem.text.strip()
                        else:
                            # 如果没有找到特定的摘要元素，尝试从整个新闻结果中提取文本
                            # 过滤掉标题、来源和图片相关的文本
                            all_text = div.get_text(separator='\n', strip=True)
                            lines = [line.strip() for line in all_text.split('\n') if line.strip()]
                            
                            # 跳过标题和来源行，提取中间的内容作为摘要
                            if len(lines) > 3:
                                # 假设前几行是标题和来源，后面是摘要
                                summary_lines = [line for line in lines if len(line) > 20 and not any(keyword in line for keyword in ['http', '来源', '作者', '发布时间'])]
                                if summary_lines:
                                    summary = ' '.join(summary_lines[:2])  # 最多取前2行作为摘要
                        
                        # 提取来源和时间（尝试多种可能的class名和标签）
                        source_elem = div.find('div', class_='c-author') or div.find('div', class_='author') or div.find('span', class_='source') or div.find('span', class_='c-gray')
                        source = source_elem.text.strip() if source_elem else ""
                        
                        # 提取封面图片（如果有，尝试多种可能的位置）
                        img_elem = div.find('img') or div.find('div', class_='c-img')
                        cover = img_elem['src'] if img_elem and 'src' in img_elem.attrs else ""
                        
                        # 添加到结果列表（去重）
                        news_results.append({
                            'title': title,
                            'summary': summary,
                            'cover': cover,
                            'original_url': link,
                            'source': source
                        })
            
            # 随机延迟1-3秒，避免被反爬
            time.sleep(random.uniform(1, 3))
        
        # 去重：根据标题和链接去重
        unique_results = []
        seen = set()
        for news in news_results:
            # 创建唯一标识
            key = (news['title'], news['original_url'])
            if key not in seen:
                seen.add(key)
                unique_results.append(news)
                # 如果达到指定数量，停止添加
                if len(unique_results) >= quantity:
                    break
        
        return unique_results
        
    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return []
    except Exception as e:
        print(f"解析错误: {e}")
        return []

# 测试函数
if __name__ == "__main__":
    keyword = "南昌"
    results = baidu_news_crawler(keyword)
    print(f"共找到 {len(results)} 条新闻")
    for i, news in enumerate(results[:5], 1):
        print(f"\n第 {i} 条新闻:")
        print(f"标题: {news['title']}")
        print(f"概要: {news['summary']}")
        print(f"封面: {news['cover']}")
        print(f"原始URL: {news['original_url']}")
        print(f"来源: {news['source']}")