import { OpenAI, ClientOptions } from "openai";
import { NextResponse } from "next/server";

const apiKey = process.env.OPENAI_KEY;

// Create the OpenAI instance with the correct options
const openaiOptions = {
  apiKey: apiKey,
};

const openai = new OpenAI(openaiOptions);

let messages = [
  {
    role: "system",
    content:
      "Jesteś asystentem/ekspertem do spraw pisania prac naukowych w składni językowej zwanej Latex.Twoim głównym zadaniem jest podawanie całkowicie poprawnych składniowo rozwiązań.Wykorzystaj w pełni swoją wiedzę z zakresu składni Latex.",
  },
];

const generatePrompts = async () => {
  //   const response = await openai.chat.completions.create({
  //     model: "gpt-3.5-turbo",
  //     messages: messages,
  //     max_tokens: 300,
  //     temperature: 0.2,
  //   });
  //   messages.push({
  //     role: "assistant",
  //     content: response["choices"][0]["message"]["content"],
  //   });
  console.log("Messages:");
  //   return response["choices"][0]["message"]["content"];
};

export async function POST(req) {
  const body = await req.json();
  //   messages.push({ role: "user", content: body.msg });
  console.log("Body:", body);

  const answear = generatePrompts();
  return new NextResponse(`${answear}`, { status: 200 });
}
