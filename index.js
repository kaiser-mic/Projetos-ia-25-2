const express = require('express');
const axios = require('axios')
const app = express();
const port = 3000
const path = require('path')

app.use(express.json())
app.use(express.static(path.join(__dirname, "public")))

const url= "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent?key=AIzaSyDLF-S5yZLDr-JI2a0fR-FaJMmVCzFxuVo"

let history = [
    {
        "role": "user",
        "parts": [
            {
                "text": "voce se chama relampago marquinhos, voce sera um assitente virtual para tirar duvidas sobre mecanica e carros. seu objetivo e ajudar pessoas leigas no assunto que estao com dificuldades. Estilo de resposta: linguagem acessivel, use exemplos quando fizer sentido, se o usuario fizer perguntas vagas ou de outros assuntos sugira um topico relacionado a mecanica automotiva. termine sempre suas mensagens com catiauuuuuuuuu e um emoji de um caror vermelho e um raio"
            }
        ]
    }
]

app.post("/chat", async(req, res) => {
    const mensagem = req.body.mensagem

    history.push({
        "role": "user",
        "parts": [
            {
                "text": mensagem
            }
        ]
    })
    try{
        const response = await axios.post(url, {contents: history}, {
            headers: {
                "Content-Type": "application/json"
            }
        
        })
        const resposta = response.data.candidates[0].content.parts[0].text

        history.push({
            "role": "model",
            "parts": [
                {
                    "text": resposta
                }
            ]
        })
        res.json({resposta}) 
    }
    catch(error){
        console.log("erro ao chamar o gemini", error)
        res.status(500).json({error: "erro ao chamar o gemini"})
    }
})
app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})