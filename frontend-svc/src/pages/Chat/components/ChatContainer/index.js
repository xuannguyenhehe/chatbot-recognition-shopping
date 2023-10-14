import defaultAvatar from "assets/DefaultAvatar.png";
import loading from "assets/loader.gif";
import ChatInput from "pages/Chat/components/ChatInput";
import { useEffect, useState, useRef } from "react";
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { useDispatch, useSelector } from "react-redux";
import { v4 as uuidv4 } from "uuid";

const ChatContainer = ({ currentChatId }) => {
  const account = useSelector((state) => state.account);
  const chats = useSelector((state) => state.chat.chats);
  const [chatName, setChatName] = useState('');
  const  { username } = account;

  const isShowLoading = useSelector((state) => state.message.isShowLoading);
  const isLoading = useSelector((state) => state.message.isLoading);
  const messages = useSelector((state) => state.message.messages);

  const dispatch = useDispatch();

  useEffect(() => {
    if (currentChatId) {
      dispatch({
        type: "message/getMessages",
        payload: {
          chatId: currentChatId,
        },
      });
      chats.forEach((chat) => {
        if (chat.id === currentChatId) {
          setChatName(chat.name);
        }
    });
    }
  }, [currentChatId, username, dispatch, chats]);

  const scrollRef = useRef(null);

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ 
      behavior: "smooth",
      inline: "end",
    });
  }, [messages]);

  const handleSendMessage = async (msg, image) => {
    dispatch({
      type: "message/sendMessage",
      payload: {
        message: msg,
        chatId: currentChatId,
        image: image,
      },
    });
  };

  return (
    <Container>
      <Row className="p-2">
          <Col sm={1} style={{"width": "5%"}}>
            <img src={defaultAvatar} alt="current Chat avatar" style={{"height": "3.1rem"}} />
          </Col>
          <Col sm={10}>
            <h3 className="m-0 p-1">{chatName}</h3>
          </Col>
      </Row>
      <Row>
      {isShowLoading ? (
        <Col style={{"textAlign": "center",}}>
          <img 
            src={loading} 
            alt="loader" 
            style={{
              "width": "120px", 
              "height": "120px",
            }}
          />
        </Col>
      ) : <Container className="m-2">
          {messages.map((message) => {
            return (
              <Row 
                ref={scrollRef} 
                key={uuidv4()} 
                className={username !== message.sender ? "d-flex flex-row my-2" : "d-flex flex-row-reverse my-2"}
              >
                <Col sm={1} style={{"width": "5%"}}>
                  <img src={defaultAvatar} alt="current Chat avatar" style={{"height": "3.1rem"}} />
                </Col>
                <Col sm={8} style={username === message.sender ? {"textAlign": "end"} : null}>
                  {message.message && (
                    <p>{message.message}</p>
                  )}
                </Col>
              </Row>
            );
          })}
          {isLoading && (
            <Row className="d-flex flex-row">
              <Col sm={1} style={{"width": "5%"}}>
                <img src={defaultAvatar} alt="current Chat avatar" style={{"height": "3.1rem"}} />
              </Col>
              <Col sm={8}>...</Col>
            </Row>
          )}
        </Container>}
      </Row>
      <ChatInput handleSendMessage={handleSendMessage} />
    </Container>
  );
};

export default ChatContainer;
