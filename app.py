from collections import namedtuple
import requests
from io import BytesIO
import html

from PIL import Image
import streamlit as st
import openai

from prompt_templates import template_dict

Expert = namedtuple('Expert', ['id', 'name', 'image'])


def ask_question(expert_id, question):
    prompt = template_dict.get(expert_id).format(user_question=question)
    response = openai.Completion.create(
        engine="davinci",
        # engine="text-davinci-001",
        # engine="text-davinci-002",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        stop=["Me:"]
    )
    return html.unescape(response["choices"][0]["text"]).capitalize()


def get_image_from_url(url: str) -> Image:
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert('RGB')
    img = img.resize((512, 512))
    return img


def make_grid(expert_list):
    for expert in expert_list:
        col1, col2 = st.columns([1, 3])
        with col1:
            st.write(expert.name)
            st.image(get_image_from_url(expert.image))
        with col2:
            question = st.text_input("Your question", key=f"{expert.id}_question")
            expert_answer_key = f"{expert.id}_answer"
            if st.button("Ask a question", key=f"{expert.id}_button"):
                st.session_state[expert_answer_key] = ask_question(expert.id, question)
            header_markdown = "####"
            expert_answer = header_markdown + " " + st.session_state.get(expert_answer_key, "").replace("\n", f"\n{header_markdown} ")
            st.write(expert_answer)
            
        st.write("#")
        st.write("#")


def main():
    st.set_page_config("Expert Bot")
    st.write("# Expert Bot")
    st.write("Choose your expert of choice and ask them a question!")

    experts_list = [
        Expert(id="steve", name="Steve Jobs", image="https://upload.wikimedia.org/wikipedia/commons/thumb/d/dc/Steve_Jobs_Headshot_2010-CROP_%28cropped_2%29.jpg/800px-Steve_Jobs_Headshot_2010-CROP_%28cropped_2%29.jpg"),
        Expert(id="pg", name="Paul Graham", image="https://pbs.twimg.com/profile_images/1824002576/pg-railsconf_400x400.jpg"),
        Expert(id="gordon", name="Gordon Ramsay", image="https://www.biography.com/.image/t_share/MTgwOTcxNDk2NDQzNzQ5NzM2/gettyimages-1148433914.jpg"),
    ]

    make_grid(experts_list)


if __name__ == '__main__':
    main()
