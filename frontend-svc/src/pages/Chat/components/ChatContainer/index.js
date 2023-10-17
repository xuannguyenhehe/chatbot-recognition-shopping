import defaultAvatar from "assets/DefaultAvatar.png";
import loading from "assets/loader.gif";
import ChatInput from "pages/Chat/components/ChatInput";
import { useEffect, useRef } from "react";
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { useDispatch, useSelector } from "react-redux";
import { v4 as uuidv4 } from "uuid";
import ImageLoad from "components/ImageLoad";


const ChatContainer = ({ currentChatUser, messages }) => {
  const account = useSelector((state) => state.account);
  const  { username } = account;

  const isShowLoading = useSelector((state) => state.message.isShowLoading);
  const isLoading = useSelector((state) => state.message.isLoading);

  const dispatch = useDispatch();
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
        chatUser: currentChatUser,
        image: image,
      },
    });
  };

  const handleCreateNewChat = async (chatUser) => {
    dispatch({
      type: "chat/createNewChat",
      payload: {
        sender: username,
        receiver: chatUser,
      },
    });
  };

  return (
    <Container>
      <Row className="mb-2">
          <Col sm={1} style={{"width": "5%"}}>
            <img src={defaultAvatar} alt="current Chat avatar" style={{"height": "3.1rem"}} />
          </Col>
          <Col sm={10}>
            <h3 className="m-0 p-1">{currentChatUser}</h3>
          </Col>
      </Row>
      <Row>
      <hr/>
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
      ) : <Container style={{
            "height": "70vh",
            "overflow": "auto",
          }}>
          {messages !== null && messages.map((message) => {
            return (
              <div 
                ref={scrollRef} 
                key={uuidv4()} 
                className={username !== message.sender ? "d-flex flex-row my-2" : "d-flex flex-row-reverse my-2"}
              >
                <Col sm={1} style={{"width": "6%"}} className="mx-2">
                  <img src={defaultAvatar} alt="current Chat avatar" style={{"height": "3.1rem"}} />
                </Col>
                <Col sm={8} style={username === message.sender ? {"textAlign": "end"} : null}>
                  <p className="m-0" style={{"fontWeight": "bold"}}>{username !== message.sender ? currentChatUser : username}</p>
                  {message.image && (
                    <ImageLoad 
                      src={message.image}
                    />
                  )}
                  {message.message && (
                    <p>{message.message}</p>
                  )}
                </Col>
              </div>
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
      <ChatInput 
        handleSendMessage={handleSendMessage} 
        messages={messages} 
        chatUser={currentChatUser}
        handleCreateNewChat={handleCreateNewChat}
      />
    </Container>
  );
};

export default ChatContainer;
