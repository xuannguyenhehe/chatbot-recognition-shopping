import ChatContainer from "components/ChatContainer";
import Contacts from "components/Contacts";
import CustomSearch from "components/CustomSearch";
import Welcome from "components/Welcome";
import { useEffect, useState, useCallback } from "react";
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";

function Chat() {
  const account = useSelector((state) => state.account);
  const {username, noTabChat} = account;

  const chats = useSelector((state) => state.chat.chats)
  const contacts = useSelector((state) => state.chat.contacts)

  let { chatId } = useParams();
  const [currentChatId, setCurrentChatId] = useState(chatId ? chatId : undefined);

  const navigate = useNavigate();
  const dispatch = useDispatch();

  const handleTabChange = useCallback((noTabChat) => {
    if (username && noTabChat === 0 && contacts.length === 0) {
      dispatch({
        type: "chat/getAllChats",
        payload: {
          username: username,
          is_get_last_message: false,
        },
      });
    }
    if (username && noTabChat === 1 && chats.length === 0) {
      dispatch({
        type: "chat/getAllChats",
        payload: {
          username: username,
          is_get_last_message: true,
        },
      });
    }
  }, [username, chats.length, contacts.length, dispatch]);

  useEffect(() => {
    if (!username) {
      navigate("/login");
    }
  }, [navigate, username]);

  useEffect(() => {
    handleTabChange(1);
  }, [username, navigate, chats.length, contacts.length, dispatch, handleTabChange]);

  const handleChatChange = (chat) => {
    navigate("/" + chat._id);
    setCurrentChatId(chat._id);
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
              chats={chats}
              contacts={contacts}
              changeChat={handleChatChange}
              handleTabChange={handleTabChange}
              noTabChat={noTabChat}
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
                {currentChatId === undefined ? (
                    <Welcome currentChatUsername={username} />
                ) : (
                    <ChatContainer currentChatId={currentChatId} />
                )}
            </Col>
        </Row>
      </Container>
  );
}

export default Chat;
