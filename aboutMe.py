import streamlit as st

def descriptionAuthor():
    col1, col2, col3 = st.beta_columns(3)
    with col3:
        st.image('logo.png')
    with col1:
        st.title('About Me', )


    st.write("# Hello there :sunglasses:")

    text = "I'm **Renato Dantas**, an automation engineer, ballistic technician, consultant and **starting the path to work as a data scientist**. \n\n **My history started on the mechanics, milling parts and CNC programming and operation**. After this, **I started on automation and the development** of mechanical equipment. \n\n My chooses took me to work as a **scientist at a ballistic laboratory**, developing ballistic protection solutions at **Dupont in Brazil**. I worked in this area for **amazing 7 years** and sometimes **I work on that as a consultant**, starting labs and training operators.\n\n But I always loved to puts **hands-on programming**. Since I learned how to program a CNC machine, **I always search to apply programming to solve tasks and create new methods to achieve new goals**. \n\n I learned some programming languages in **college**, like C++, C#, JS, but **was Python that makes me discover a new area to create solutions and solve problems:** ***Machine Learning!*** \n\n It's amazing to learn how to **get insights just by manipulating data** with such a huge number of easy useful libraries like **Pandas, Numpy, Matplolib, etc**. \n\n This new area became **my passion** and my hobby too.\n**I started to learn and solve real-world problems** in my role at Dupont, **making predictions with regression models** and **creating some applications** to help me do **extract the best of my data** in the lab. \n\n I'm a person that is **always learning new things**. This week I saw an article about **Streamlit** and here I am! \n\n"

    st.write(text)
    st.write('Well, if you are **interested to know more about me**, please send me an invitation on **LinkdIn**. Just click on the ***link below***. \n\n **https://www.linkedin.com/in/dantasrenato**')

    st.write('You can find the **code for this page on my GitHub:**\n\n **https://github.com/Renato-Dantas**')
    st.write("**Feel free to contribute!**\n\n***Best regards!***\n\n***Renato Dantas***")





