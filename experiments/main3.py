from openai import OpenAI
import faiss
import numpy as np
import os
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
load_dotenv()
def load_documents(docs_dir="docs"):
    """
    从当前脚本同级目录下的 docs 文件夹中读取所有 .txt 文件
    返回 documents 列表
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docs_path = os.path.join(base_dir, docs_dir)

    documents = []

    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"docs 文件夹不存在: {docs_path}")

    for filename in os.listdir(docs_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(docs_path, filename)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()

                if content:
                    documents.append(content)

    if not documents:
        raise ValueError(f"docs 文件夹下没有可用的 txt 文件: {docs_path}")

    return documents

# 数据
# documents =[
# "二次元是ACGN（动画、漫画、游戏、轻小说）亚文化圈的专门用语，原指二维空间构成的虚拟世界，现泛指由平面视觉作品构建的幻想世界及其衍生文化。其核心涵盖动画、漫画、电子游戏及轻小说等作品，角色多以“纸片人”形象呈现，题材涵盖历史、奇幻、科幻等多元领域。该概念虽与ACGN紧密相关，但本质上是人类幻想的虚拟世界表达，并不等同于ACGN本身。“二次元”最早发源于1979年的日本。90年代初，中国的二次元产业开始萌芽，经过十几年的孕育、成长，二次元产业在中国一步步明朗起来。从2002年开始，国家开始出台一系列政策，扶持国内原创动漫，快速提高了国产动画的数量。随着互联网发展及Z世代崛起，二次元文化从小众圈层扩散至主流社会，形成覆盖创作、传播、消费的完整产业链。衍生出漫展、虚拟偶像、主题餐饮、周边商品及文旅融合等业态。其文化特性体现为强情感共鸣与社群属性，通过IP授权、跨界联名等方式渗透至商业地产、快消品等领域。国内政策同步引导产业规范化发展，如上海出台措施加强未成年人保护及知识产权管理，推动二次元经济从兴趣消费升级为城市新消费引擎。二次元影响力扩大是一个双向过程。一方面，它用图像简化现实的细节，将个性表现到极致。另一方面，青少年正处在表达个性的时期，他们认同文艺作品，就会参加漫展、收藏动漫周边、展开衍生创作。这种基于平面符号和想象世界的文化互动孕育出二次元作品，力图唤起人们想象的热情，以简化线条烘托无法言传的韵味。",
# "90年代初，中国的二次元产业开始萌芽，经过十几年的孕育、成长，二次元产业在中国一步步明朗起来。从2002年开始，国家开始出台一系列政策，扶持国内原创动漫，快速提高了国产动画的数量。尤其是在2012年，文化部发布了《“十二五”时期国家动漫产业发展规划》，这是动漫产业首次进行单列规划。为了支持国内原创二次元作品，政府甚至出台了一系列规范措施。如：从17点到21点，必须播放国产动漫节目。加大动漫行业整顿，相关日本动漫被暂时禁播，这一系列的政策也为国漫的发展提供了便利。移动互联网的发展近两年移动互联网的发展让二次元的内容传播速度更快，受众范围不断扩大。在互联网+的大环境下，漫画也被以更多的方式呈现出来，产生了众多网站和APP，还有论坛、咨询、视频等各个领域。其中“弹幕”的兴起更是网罗了一众二次元的爱好者。“弹幕”慢慢地已经成为了一种文化潮流，在观影的过程中随时留言、随时评论，进行实时互动。90后开始工作了中国二次元用户的分布已经进入到90后时代。随着90后的最后一代也进入劳动，他们信奉追捧的二次元文化，作为一种独特的文化现象，从默默边缘到如今标杆文化，也跟着90后一起迈入社会发展洪流。中国人的生活当中已经越来越多的人是属于二次元消费的人群。而这些二次元人也有购买的能力，比如喜欢动漫人物，那么也会购买带有动漫形象的衍生品。还有就是动漫主题的餐厅，这些都是属于二次元人群消费的场所。人群规模据估算，2016年国内核心“二次元”用户规模达7000万人，泛二次元用户规模达2亿人。也就是说，每20个中国人中就有1个是“二次元”重度粉丝，有3个是轻度粉丝。从年龄构成上看，最早接触“二次元”的80后正逐渐“老去”，90后和00后已是“二次元”用户主力人群，占到90%以上。随着大众传媒的发展，各种日本动漫产品陆续传到国内，影响了国内的年轻人群体。近年来，由于资本入侵、互联网发展，还有“二次元”群体的迭代更新，“二次元”文化表现出了向主流文化靠拢的趋势。“二次元”产品类型已不局限于动画、漫画、游戏等，声优、漫展、角色扮演、线下演唱会、漫画周边手办、古风音乐等也占据了重要地位。早期，日系产品占据国内“二次元”的主要消费市场，但随着国产漫画的追赶，也拥有了相当数量粉丝，开始与日系产品相抗衡。相关漏洞一段时间来，广义的“二次元”领域，不乏一些“劣币驱良币”的恶性竞争。个别带有色情、血腥、污秽的动漫、短视频、直播内容借助互联网快速传播，点对点影响年轻人，扩散负能量。国家新闻出版广电总局副局长田进最近在第四届中国网络视听大会主论坛上明确指出：网络视听节目播出平台要坚持高标准、严要求，倒逼创作主体努力创新、提高质量，将“劣币”逐出市场，给“良币”更好的发展空间。对“三俗”说不，2016年国内“二次元”平台已进一步加强自审。百度贴吧、B站等对相关业务进行了梳理、整合、优化。社会评价二次元影响力扩大是一个双向过程。一方面，其题材本身源于生活，它用图像简化现实的细节，把幻想外化，将个性表现到极致，并借助互联网将拥有类似特质的用户连接到一起。另一方面，青少年正处在希望以新形式表达个性的时期，他们认同文艺作品中的形象，就会参加漫展、收藏动漫周边、展开衍生创作。这种基于平面符号和想象世界的双向文化互动孕育出二次元作品，二次元作品特质在于图像语言的丰富与文字的极简。故事通常设定在遥远的想象世界，反映年轻人天马行空的浪漫气质。这类作品以细致入微的图像取代具体文字描写，以图像语言进行“意会”式传达。作品中出现的文字多半是对话和象声词，造就故事内容直白简约、画面风格精致唯美。它们力图唤起人们想象的热情，以简化线条烘托无法言传的韵味。",
# "引申含义ACGNACGN是英文Animation、Comic、Game、Novel的缩写，其中A表示的是动画（特指日本动画）、C表示的是动漫（通常指日本漫画）、G表示的是游戏（通常指电玩游戏）、N表示的是小说（主要指轻小说）， [7]是从ACG扩展而来的新词汇，主要流行于华语文化圈。“二次元”最常见的引申含义就是泛指ACGN，此用法侧重于体现二次元世界的载体，如“你喜欢什么二次元作品”，“花仙子是二次元人物”。虽然大多数情况下二次元可以代替ACGN，但须注意的是，二次元和ACGN并不完全相同，前者侧重强调虚拟与现实的不同，后者侧重强调作品的体裁。二次元宅作为一个指称特定文化主体的名词，是由“二次元”和“宅”这两个词语合并而成的。 [5]划分名词二次元，即二维。“次元”即“维度”，是英文单词dimension的两种翻译。这种说法诞生于日本，早期的少女（少年）漫画、动画、美少女游戏都是由二维图像构成，其画面是一个平面，所以被称为是“二次元世界”，简称“二次元”。与之相对的是“三次元”，即“我们所存在的这个次元”，也就是现实世界。划分名词按世界划分二次元：虚拟世界，如动画、漫画、游戏、小说、动漫世界三次元：现实世界按载体划分二次元：动画、漫画、游戏（以galgame和日系卡牌游戏等为主，包括但不限于此）、小说（包括但不限于轻小说）、虚拟偶像、部分电影、部分电视剧以及其衍生同人创作及周边产品等。2.5次元：真人表演与人造动画合成作品，以及由ACGN作品衍生而来的舞台剧等真人表演作品，Cosplay也认为是2.5次元的主要表现形式。 [1]三次元：真人影视剧次元联系二次元是指人类幻想出来的唯美世界，用各种憧憬的体现虐袭观赏者的视觉体验，数学空间纬度上，本质其实还是三次元世界的人类心中模糊的美好印象。与二次元相对的三次元，除了用于指现实世界之外，也用于指现实的人物、事物。由现实世界的人物、事物所诞生的图像、影视作品，属于三次元，而不属于二次元，因此真人电影、电视剧、真人照片，因为其给予人心中最直观的认知。个性文化此含义为中国动漫产业发展过程中衍生出来的特殊含义，此时二次元专指“个性”、“潮流”、“年轻”，是中国资本方为了炒热ACGN产业而赋予二次元的新含义，ACGN圈内很少采用此用法，同时“二不起，二不起”就是嘲讽这种用法。萌二文化萌二为“萌萌二次元”的缩写，多带贬义色彩。此含义是一部分思想不成熟的动漫爱好者过分神化“二次元”而对二次元赋予的新含义，与御宅文化有相似之处，特点为具有很强的排他性、优越性，如“高贵的二次元才不屑于与三次元同流合污”。",
# ]
documents = load_documents()

def init_model():
    global model,client
    #加载M3E模型 先检查本地是否存在
    local_model_path = "local_m3e_model"
    if os.path.exists(local_model_path):
        print(f"加载本地模型: {local_model_path}")
        model = SentenceTransformer(local_model_path)
    else:
        print(f"本地模型不存在，从Hugging Face下载...")
        model = SentenceTransformer("moka-ai/m3e-base")
        print(f"模型下载完成，保存到: {local_model_path}")
        model.save_pretrained(local_model_path)
    
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"
    )

chunks_map_path = "chunks_map.npy"
# 初始化索引与映射关系
def init_index(documents):
    global index,document_to_chunks,chunks_to_document,all_chunks
    #使用faiss创建向量索引 先检查本地是否存在
    local_index_path = "local_index"
    if os.path.exists(local_index_path) and os.path.exists(chunks_map_path):
        print(f"加载本地索引和映射: {local_index_path},{chunks_map_path}")
        index = faiss.read_index(local_index_path)
        #加载映射关系
        mapping_data = np.load(chunks_map_path,allow_pickle=True).item()
        document_to_chunks = mapping_data["document_to_chunks"]
        chunks_to_document = mapping_data["chunks_to_document"]
        all_chunks = mapping_data["all_chunks"]
    else:
        print(f"本地索引不存在，创建新的索引...")
        for doc_id,doc in enumerate(documents):
            chunks =chunk_document(doc)

            document_to_chunks[doc_id] = []
            for chunk in chunks:
                chunk_id = len(all_chunks)
                all_chunks.append(chunk)
                document_to_chunks[doc_id].append(chunk_id)
                chunks_to_document[chunk_id] = doc_id
        chunk_embeddings = get_embedding(all_chunks)
        index = faiss.IndexFlatL2(chunk_embeddings.shape[1])
        index.add(chunk_embeddings)
        print(f"索引创建完成，保存到: {local_index_path}")
        faiss.write_index(index,local_index_path)

        mapping_data = {
            "document_to_chunks":document_to_chunks,
            "chunks_to_document":chunks_to_document,
            "all_chunks":all_chunks
        }
        np.save(chunks_map_path,mapping_data)
        print(f"映射关系保存到: {chunks_map_path}")

# 文档切片
def chunk_document(text,max_chars=500,overlap=100):
    if len(text) <= max_chars:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars,len(text))
        chunks.append(text[start:end])
        start = end - overlap

        if start < 0:
            start = 0
        if start >= len(text) or end >= len(text):
            break
    return chunks

# 获取向量(支持文本列表或纯文本)
def get_embedding(texts):
    if isinstance(texts,list):
        return model.encode(texts,convert_to_numpy=True)
    else:
        return model.encode([texts],convert_to_numpy=True)

# 文档与chunks的映射关系
document_to_chunks = {}
chunks_to_document = {}
all_chunks = []

def retrieve_docs(query,index,k=3):
    query_embedding = get_embedding(query)
    distances,chunk_indices = index.search(query_embedding,k)
    # 获取包含这些chunks的原始文档ID
    retrieved_doc_ids = set()
    retrieved_chunks = []
    for chunk_idx in chunk_indices[0]:
        if chunk_idx >=0 and chunk_idx < len(all_chunks):
            doc_id = chunks_to_document.get(int(chunk_idx))
            if doc_id is not None:
                retrieved_doc_ids.add(doc_id)
                retrieved_chunks.append(all_chunks[chunk_idx])
    return list(retrieved_doc_ids),retrieved_chunks

# 请求LLM
def generate_response(context,query):
    prompt = f"请根据以下内容回答问题：{context}\n问题：{query}"
    response = client.chat.completions.create(
        model="deepseek-v4-flash",
        messages=[
            {"role": "system", "content": "你是一个专业的知识库问答助手。严格回答问题，不知道就回答不知道。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def main():
    init_model()
    init_index(documents)

    query = "动漫和动画、漫画有何区别？"
    retrieved_doc_ids,retrieved_chunks = retrieve_docs(query,index)
    print(f"找到的相关文档ID: {retrieved_doc_ids}")
    context = "\n".join(retrieved_chunks)
    print(f"context: {context}")
    answer = generate_response(context,query)
    return answer
    # indices: [[2 1 0]]

if __name__ == "__main__":
    answer = main()
    print(f"\n模型回答: {answer}")
