import ChatContainer from "pages/Chat/components/ChatContainer";
import Contacts from "pages/Chat/components/Contacts";
import CustomSearch from "components/CustomSearch";
import Welcome from "pages/Chat/components/Welcome";
import { useEffect, useState, useCallback } from "react";
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { useDispatch, useSelector } from "react-redux";
import { useNavigate, useParams } from "react-router-dom";

function Chat() {
  const account = useSelector((state) => state.account);
  const {username, noTabChat} = account;
  let { chatUser } = useParams();

  const chats = useSelector((state) => state.chat.chats)
  const contacts = useSelector((state) => state.chat.contacts)
  const searchUsers = useSelector((state) => state.chat.searchUsers)
  const messages = useSelector((state) => state.message.messages);

  const [currentChatUser, setCurrentChatUser] = useState(chatUser ? chatUser : undefined);

  const navigate = useNavigate();
  const dispatch = useDispatch();

  useEffect(() => {
    if (currentChatUser) {
      dispatch({
        type: "message/getMessages",
        payload: {
          chatUser: currentChatUser,
        },
      });
    }
  }, [currentChatUser, dispatch]);

  useEffect(() => {
    setCurrentChatUser(chatUser)
  }, [chatUser])

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
    navigate("/t/" + chat.name);
    setCurrentChatUser(chat.name);
  };

  const changeTab = (index) => {
    dispatch({
      type: "account/saveState",
      payload: {
        noTabChat: index,
      },
    });
    handleTabChange(index);
  }

  const handleSearchUsers = (keyword) => {
    dispatch({
      type: "account/handleSearch",
      payload: {
        keyword: keyword,
      },
    });
  }

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
                  changeform={handleSearchUsers}
                  direction={"left"}
                  changeTab={changeTab}
                />
            </Container>
            <Contacts
              chats={chats}
              contacts={contacts}
              chatUser={chatUser}
              searchUsers={searchUsers}
              changeChat={handleChatChange}
              handleTabChange={handleTabChange}
              noTabChat={noTabChat}
              messages={messages}
            />
          </Col>
          
            <Col 
                sm={9}
                style={{
                    "background": "#00000076",
                    "border": "1px solid #303030",
                    "borderRadius": "3px"
                }}
                className="p-4"
            >
                {currentChatUser === undefined ? (
                    <Welcome currentChatUsername={username} />
                ) : (
                    <ChatContainer 
                      currentChatUser={currentChatUser} 
                      messages={messages}
                    />
                )}
            </Col>
        </Row>
      </Container>
  );
}

export default Chat;
