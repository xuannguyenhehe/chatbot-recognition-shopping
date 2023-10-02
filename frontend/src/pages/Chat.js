import { useState, useEffect } from "react";
import styled from "styled-components";
import { useNavigate } from "react-router-dom";
import Contacts from "../components/Contacts";
import Welcome from "../components/Welcome";
import ChatContainer from "../components/ChatContainer";
import { useDispatch, useSelector } from "react-redux";

function Chat() {
  const chats = useSelector((state) => state.chat.chats);
  const [contacts, setContacts] = useState(chats);
  const [currentChat, setCurrentChat] = useState(undefined);
  const currentUser = localStorage.getItem("username");
  const navigate = useNavigate();
  const dispatch = useDispatch();

  useEffect(() => {
    if (!currentUser) {
      navigate("/login");
    }
  }, [navigate, currentUser]);

  useEffect(() => {
    if (chats.length) {
      setContacts(chats)
    }
  }, [chats]);

  useEffect(() => {
    if (currentUser && contacts.length === 0) {
      dispatch({
        type: "chat/getAllChats",
        payload: {
          username: currentUser,
        },
      });
    }
  }, [currentUser, navigate, contacts.length, dispatch]);

  const handleChatChange = (chat) => {
    setCurrentChat(chat);
  };

  return (
    <>
      <Container>
        <div className="container">
          <Contacts
            contacts={contacts}
            currentUser={currentUser}
            currentImage={null}
            changeChat={handleChatChange}
          />
          {currentChat === undefined ? (
            <Welcome currentUsername={currentUser?.username || ""} />
          ) : (
            <ChatContainer chatId={currentChat._id} chatName={currentChat.name} />
          )}
        </div>
      </Container>
    </>
  );
}

const Container = styled.div`
  height: -webkit-fill-available;
  width: 100vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1rem;
  align-items: center;
  background-color: #0e0e11;
  .container {
    height: 100vh;
    width: 100vw;
    background-color: #00000076;
    display: grid;
    grid-template-columns: 20% 80%;

    @media screen and (min-width: 720px) {
      grid-template-columns: 35% 65%;
      grid-template-rows: none;
      width: 85vw;
      height: 100vh;
    }
    @media screen and (min-width: 1100px) {
      grid-template-columns: 28% 72%;
    }
  }
`;

export default Chat;
