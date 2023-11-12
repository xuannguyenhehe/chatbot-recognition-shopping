import defaultAvatar from "assets/DefaultAvatar.png";
import loading from "assets/loader.gif";
import ImageLoad from "components/ImageLoad";
import ChatInput from "pages/Chat/components/ChatInput";
import { useEffect, useRef, useState, useCallback } from "react";
import { Button, Col, Container, Figure, Modal, Row } from "react-bootstrap";
import ImageUploading from "react-images-uploading";
import { useDispatch, useSelector } from "react-redux";
import { v4 as uuidv4 } from "uuid";


const ChatContainer = ({ currentChatUser, messages }) => {
  const account = useSelector((state) => state.account);
  const  { username } = account;

  const isShowLoading = useSelector((state) => state.message.isShowLoading);
  const isLoading = useSelector((state) => state.message.isLoading);
  const currentMessage = useSelector((state) => state.message.currentMessage);
  const currentImage = useSelector((state) => state.message.currentImage);
  const isShowImageUploadArea = useSelector((state) => state.message.isShowImageUploadArea);

  const [choseOptionImage, setChoseOptionImage] = useState(null);
  const [isShowImageOptionModal, setIsShowImageOptionModal] = useState(false);

  const dispatch = useDispatch();
  const scrollRef = useRef(null);

  const handleChangeMessage = useCallback((message) => {
    dispatch({
      type: "message/saveState",
      payload: {
        currentMessage: message,
      },
    });
  }, [dispatch])

  const handleChangeImage = useCallback((image) => {
    dispatch({
      type: "message/saveState",
      payload: {
        currentImage: image,
      },
    });
  }, [dispatch])

  const handleIsShowImageUploadArea = useCallback((isShow) => {
    dispatch({
      type: "message/saveState",
      payload: {
        isShowImageUploadArea: isShow,
      },
    });
  }, [dispatch])

  const onChangeCurrentImage = (imageList) => {
    imageList.forEach((element) => {
      if (element.dataURL) {
        handleChangeImage(element)
        handleIsShowImageUploadArea(false)
      }
    });
  };

  const handleError = (errors, _) => {
    console.log(errors);
  };

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ 
      behavior: "smooth",
      inline: "end",
    });
  }, [messages]);

  const handleSendMessage = async (msg, image, isForceSend) => {
    dispatch({
      type: "message/sendMessage",
      payload: {
        message: msg,
        chatUser: currentChatUser,
        image: image,
        isForceSend: isForceSend,
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

  const onMouseEnter = (e) => {
    e.target.style.border = '3px solid green';
    e.target.style.cursor = 'pointer';
  }
  const onMouseLeave = (e) => {
    e.target.style.border = '';
    e.target.style.cursor = '';
  }

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
                  {message.options !== null && message.options?.length && message.options.map((option, indexOption) => {
                    return (
                      <Figure
                        key={indexOption}
                        style={{ 
                          position: "relative", 
                          marginRight: "5px", 
                        }}
                        onMouseEnter={message.is_option_action ? onMouseEnter: null}
                        onMouseLeave={onMouseLeave}
                        onClick={() => {
                          setChoseOptionImage(option)
                          setIsShowImageOptionModal(true)
                        }}
                      >
                        <ImageLoad 
                          src={option}
                        />
                      </Figure>
                    )})
                  }
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
      <Modal show={isShowImageUploadArea}>
        <Modal.Header closeButton>
          <Modal.Title>Bạn có ảnh mẫu không?</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            Việc có ảnh mẫu sẽ giúp chatbot tìm kiếm ảnh phù hợp nhất với bạn?
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => {
            handleIsShowImageUploadArea(false);
            handleSendMessage(currentMessage, currentImage, true)
          }}>
            Không
          </Button>
          <ImageUploading
            multiple={false}
            value={currentImage}
            onChange={onChangeCurrentImage}
            onError={handleError}
          >
            {({ onImageUpload }) => (
              <div>
                <Button variant="primary" onClick={onImageUpload}>Có</Button>
              </div>
            )}
          </ImageUploading>
        </Modal.Footer>
      </Modal>
      <Modal show={isShowImageOptionModal}>
        <Modal.Header closeButton>
          <Modal.Title>Ảnh này làm bạn hài lòng chứ?</Modal.Title>
        </Modal.Header>
        <Modal.Body style={{"alignSelf": "center"}}>
          <ImageLoad 
            src={choseOptionImage}
            size={200}
          />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setIsShowImageOptionModal(false)}>
            Không
          </Button>
          <Button variant="secondary" onClick={() => setIsShowImageOptionModal(false)}>
            Có
          </Button>
        </Modal.Footer>
      </Modal>
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
