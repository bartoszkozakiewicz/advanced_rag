"use client";
import React, { useEffect, useRef, useState } from "react";
import { axiosInstance } from "@/utils/axiosInstance";

const Chat = () => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [messages, setMessages] = useState([
    { sender: "bot", msg: "Witaj w naszym chacie!" },
  ]);
  const [newMessage, setNewMessage] = useState("");
  const [answearing, setAnswearing] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    // @ts-ignore
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (isExpanded) {
      scrollToBottom();
    }
  }, [messages, isExpanded]);

  console.log("process.env.FAST_API", process.env.PUBLIC_FAST_API);
  const sendMessage = async (e: any) => {
    e.preventDefault();
    if (!newMessage.trim()) return;
    setMessages([...messages, { msg: newMessage, sender: "user" }]);
    setNewMessage("");
    setAnswearing(true);
    try {
      const response = await axiosInstance
        .post(`http://127.0.0.1:8000/chat`, {
          message: newMessage,
        })
        .then((response) => {
          console.log("Response:", response.data.message);
          setMessages([
            ...messages,
            { msg: newMessage, sender: "user" },
            { msg: response.data.message, sender: "bot" },
          ]);
        })
        .catch((error) => {
          console.log("Error:", error);
        })
        .finally(() => {
          setAnswearing(false);
        });
    } catch (err) {
      console.log("gowno");
    }
  };
  return (
    <div
      className={`fixed bottom-4 right-4 flex flex-1 flex-col items-end  ${
        isExpanded ? "max-h-screen" : "max-h-16"
      } transition-max-height duration-500 ease-out`}
    >
      {isExpanded && (
        <div className="flex h-[500px] flex-col justify-between rounded-lg bg-white shadow-lg">
          <div className="border-b  border-gray-200 p-4">
            <h2 className="text-lg font-semibold">AI Chat</h2>
          </div>
          <div className="h-[500px] max-h-[500px] w-[450px] max-w-[450px]  overflow-y-scroll p-4">
            {messages.map((msg, index) => (
              <div key={index} className="mt-2">
                <div
                  className={`rounded-lg  p-2 ${
                    msg.sender === "user"
                      ? "bg-blue-100 text-right text-blue-800"
                      : "bg-orange-100 text-orange-800"
                  }`}
                >
                  {msg.msg}
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </div>
          <div className="w-[450px] max-w-[450px] border-t border-gray-200 p-4">
            <input
              disabled={answearing}
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              className="w-full rounded-lg border border-gray-300 p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Napisz wiadomość..."
            />
            <button
              // type="submit"
              className="mt-2 w-full rounded-lg bg-blue-500 py-2 px-4 font-bold text-white transition-colors duration-150 hover:bg-blue-700"
              onClick={sendMessage}
            >
              Wyślij
            </button>
          </div>
        </div>
      )}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="z-10 mt-2 rounded-full bg-blue-500 py-2 px-4 font-bold text-white transition-colors duration-150 hover:bg-blue-700"
      >
        {isExpanded ? "Zwiń" : "Rozwiń"} chat
      </button>
    </div>
  );
};

export default Chat;
