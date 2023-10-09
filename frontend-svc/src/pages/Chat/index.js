import ChatContainer from "components/ChatContainer";
import Contacts from "components/Contacts";
import Welcome from "components/Welcome";
import { useEffect, useState } from "react";
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Container from 'react-bootstrap/Container';
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";
import CustomSearch from "components/CustomSearch"
import styles from "./index.scss";

function Chat() {
  const chats = useSelector((state) => state.chat.chats);
  const [contacts, setContacts] = useState(chats);
  const [currentChat, setCurrentChat] = useState(undefined);
  const currentUser = localStorage.getItem("user");
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
      <Container style={{
            "margin": "1px",
            "color": "white",
            "maxWidth": "100vw",
          }}>
        <Row>
          <Col 
            sm={3} 
            style={{
              "background": "rgb(24, 25, 26)",
              "minHeight": "90vh",
              "overflow": "auto",
              "border": "1px solid #303030",
              "borderRadius": "3px",
            }}
          >
            <Container
                style={{
                    "padding": "10px 0px",
                }}
            >
                <CustomSearch
                    label={"Search"}
                    // value={formik.values.name_like}
                    // changeform={(value) => {
                    //     handleChangeForm(value, "name_like");
                    // }}
                    direction={"left"}
                />
            </Container>
            <Contacts
                contacts={contacts}
                currentUser={currentUser}
                currentImage={null}
                changeChat={handleChatChange}
            />
          </Col>
          
            <Col 
                sm={9}
                style={{
                    "background": "#00000076",
                    "border": "1px solid #303030",
                    "borderRadius": "3px"
                }}
            >
                {currentChat === undefined ? (
                    <Welcome currentUsername={currentUser?.username || ""} />
                ) : (
                    <ChatContainer chatId={currentChat._id} chatName={currentChat.name} />
                )}
            </Col>
        </Row>
      </Container>
  );
}

export default Chat;
