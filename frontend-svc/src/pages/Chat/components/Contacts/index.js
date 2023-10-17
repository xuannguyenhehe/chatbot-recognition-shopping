import defaultAvatar from "assets/DefaultAvatar.png";
import React, { useState, useEffect } from "react";
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import { IoIosContact } from 'react-icons/io';
import { SiChatbot } from 'react-icons/si';
import { useDispatch, useSelector } from "react-redux";


const Contacts = ({ chats, contacts, chatUser, searchUsers, changeChat, handleTabChange, noTabChat, messages }) => {
  const dispatch = useDispatch();
  const account = useSelector((state) => state.account);
  const {username} = account;
  const [showUsers, setShowUsers] = useState(contacts);

  useEffect(() => {
    if (searchUsers.length) {
      setShowUsers(searchUsers);
    } else {
      setShowUsers(contacts);
    }
  }, [searchUsers, contacts])

  const changeTab = (index) => {
    dispatch({
      type: "account/saveState",
      payload: {
        noTabChat: index,
      },
    });
    handleTabChange(index);
  }

  const changeCurrentChat = (contact) => {
    changeChat(contact);
    changeTab(1);
  };

  return (
    <>
      <Container className="p-0">
        <Row style={{"height": "75vh"}}>
          <Container>
          {noTabChat === 0 && showUsers.map((contact, index) => {
              return (
                <Row 
                  key={index}
                  className="m-3 p-2"
                  onClick={() => changeCurrentChat(contact)}
                >
                  <Col sm={3} style={{"width": "20%"}}>
                    <img src={contact.avatarImage || defaultAvatar} alt="" style={{"height": "3.1rem"}} />
                  </Col>
                  <Col sm={9}>
                    <h6>{contact.name}</h6>
                  </Col>
                </Row>
              );
            })}
            {(messages === null || messages === undefined) && noTabChat === 1 && chatUser && (
              <Row 
                className="m-3 p-2"
                style={{
                  "backgroundColor": "blue",
                  "borderRadius": "10px",
                }}
              >
                <Col sm={3} style={{"width": "20%"}}>
                  <img src={defaultAvatar} alt="" style={{"height": "3.1rem"}} />
                </Col>
                <Col sm={9}>
                  <h5>{chatUser}</h5>
                </Col>
              </Row>
            )}
            {messages !== null && noTabChat === 1 && chats.map((contact, index) => {
              if (contact.name === chatUser) {
                return (
                  <Row 
                    key={index}
                    className="m-3 p-2"
                    onClick={() => changeCurrentChat(contact)}
                    style={{
                      "backgroundColor": "blue",
                      "borderRadius": "10px",
                    }}
                  >
                    <Col sm={3} style={{"width": "20%"}}>
                      <img src={contact.avatarImage || defaultAvatar} alt="" style={{"height": "3.1rem"}} />
                    </Col>
                    <Col sm={9}>
                      <h5>{contact.name}</h5>
                      <h6>{contact.last_message_user === username ? "Me:" : contact.last_message_user} {contact.last_message}</h6>
                    </Col>
                  </Row>
                );
              } else return null;
            })}
            {noTabChat === 1 && chats.map((contact, index) => {
              if (contact.name !== chatUser) {
                return (
                  <Row 
                    key={index}
                    className="m-3 p-2"
                    onClick={() => changeCurrentChat(contact)}
                    style={{
                      "borderRadius": "10px",
                    }}
                  >
                    <Col sm={3} style={{"width": "20%"}}>
                      <img src={contact.avatarImage || defaultAvatar} alt="" style={{"height": "3.1rem"}} />
                    </Col>
                    <Col sm={9}>
                      <h5>{contact.name}</h5>
                      <h6>{contact.last_message_user === username ? "Me:" : contact.last_message_user} {contact.last_message}</h6>
                    </Col>
                  </Row>
                );
              } else return null;
            })}
          </Container>
        </Row>
        <Row 
          style={{
            "backgroundColor": "#18191a",
            "borderTop": "0.2px solid #ffffff15",
            "textAlign": "center",
          }}
          className="p-2"
        >
          <Col sm={6}>
            <IoIosContact 
              style={{
                "height": "3.1rem",
                "width": "3.1rem",
                "borderRadius": "50%",
                "color": noTabChat === 0 ? "blue" : "white",
              }}
              onClick={() => changeTab(0)}
            />
          </Col>
          <Col sm={6}>
            <SiChatbot 
              style={{
                "height": "3.1rem",
                "width": "3.1rem",
                "borderRadius": "50%",
                "color": noTabChat === 1 ? "blue" : "white",
              }}
              onClick={() => changeTab(1)}
            />
          </Col>
        </Row>
      </Container>
    </>
  );
};

export default Contacts;
