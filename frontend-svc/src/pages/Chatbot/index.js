import ChatContainer from "components/ChatContainer";
import Contacts from "components/Contacts";
import CustomSearch from "components/CustomSearch";
import Welcome from "components/Welcome";
import { useEffect, useState } from "react";
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

function ChatBot() {
  const account = useSelector((state) => state.account);
  const [username, role, noTab] = [account.username, account.role, account.noTab];

  const chats = useSelector((state) => state.chat.chats);
  const [contacts, setContacts] = useState(chats);

  const [currentChat, setCurrentChat] = useState(undefined);
  const currentChatUser = localStorage.getItem("user");

  const navigate = useNavigate();
  const dispatch = useDispatch();

  useEffect(() => {
    if (!username) {
      navigate("/login");
    }
  }, [navigate, username]);

  useEffect(() => {
    if (chats.length) {
      setContacts(chats)
    }
  }, [chats]);

  useEffect(() => {
    if (username && contacts.length === 0) {
      dispatch({
        type: "chat/getAllChats",
        payload: {
          username: username,
        },
      });
    }
  }, [username, navigate, contacts.length, dispatch]);

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
              "minHeight": "80vh",
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
              changeChat={handleChatChange}
              noTab={noTab}
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
                    <Welcome currentChatUsername={currentChatUser?.username || ""} />
                ) : (
                    <ChatContainer chatId={currentChat._id} chatName={currentChat.name} />
                )}
            </Col>
        </Row>
      </Container>
  );
}

export default ChatBot;
