import defaultAvatar from "assets/DefaultAvatar.png";
import cameraImage from "assets/camera.png";
import Chat from "assets/chat.png";
import React, { useState } from "react";
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useNavigate } from "react-router-dom";
import styled from "styled-components";

const Contacts = ({ contacts, currentUser, currentImage, changeChat }) => {
  const [currentSelected, setCurrentSelected] = useState("");
  const [showEditButton, setShowEditButton] = useState(false);
  const navigate = useNavigate();

  const changeCurrentChat = (index, contact) => {
    setCurrentSelected(index);
    changeChat(contact);
  };

  const handleEditButton = () => {
    navigate("/setAvatar");
  };

  return (
    <>
      <Container className="p-0">
        
        {/* <div className="brand">
          <img src={Chat} alt="logo" />
          <h3>Chat</h3>
        </div> */}
        <Row 
          className="contacts"
          style={{"height": "80vh"}}
        >
          <Container>
            <Row onClick={() => changeCurrentChat(1, "contact")}>
              <Col className="avatar" sm={3} style={{"width": "20%"}}>
                <img src={defaultAvatar} alt="" style={{"height": "3.1rem"}} />
              </Col>
              <Col className="username" sm={9}>
                <Row>abc</Row>
                <Row>uu</Row>
              </Col>
            </Row>
          </Container>
          {contacts.map((contact, index) => {
            return (
              <div
                key={contact._id}
                className={`contact ${index === currentSelected ? "selected" : ""}`}
                onClick={() => changeCurrentChat(index, contact)}
              >
                <div className="avatar">
                  <img src={contact.avatarImage || defaultAvatar} alt="" />
                </div>
                <div className="username">
                  <h3>{contact.name}</h3>
                </div>
              </div>
            );
          })}
        </Row>
        <Row 
          className="current-user"
          style={{
            "backgroundColor": "#18191a",
            "borderTop": "0.2px solid #ffffff15",
          }}
        >
          <Col
            className="avatar"
            onMouseEnter={() => setShowEditButton(true)}
            onMouseLeave={() => setShowEditButton(false)}
            style={{
              "height": "3.1rem",
            }}
            sm={2}
          >
            <img 
              src={currentImage || defaultAvatar} alt="avatar" 
              style={{"height": "3.1rem"}}
            />

            {showEditButton && (
              <div className="camera-img" onClick={handleEditButton}>
                <img src={cameraImage} alt="camera" />
              </div>
            )}
          </Col>
          <Col className="username p-2" sm={10}>
            <h5>{currentUser}</h5>
          </Col>
        </Row>
      </Container>
    </>
  );
};

// const Container = styled.div`
//   display: grid;
//   grid-template-rows: 10% 80% 10%;
//   overflow: hidden;
//   background-color: #18191a;
//   .brand {
//     display: flex;
//     align-items: center;
//     gap: 1rem;
//     justify-content: center;
//     /* padding: 1.8rem 0; */
//     img {
//       height: 3rem;
//     }
//     h3 {
//       color: #e4e6eb;
//       text-transform: uppercase;
//       display: none;
//     }
//     @media screen and (min-width: 720px) {
//       h3 {
//         display: block;
//       }
//     }
//   }

//   .contacts {
//     display: flex;
//     flex-direction: column;
//     overflow: auto;
//     gap: 0.8rem;
//     &::-webkit-scrollbar {
//       width: 0.2rem;
//       &-thumb {
//         background-color: #ffffff39;
//         width: 0.1rem;
//         border-radius: 1rem;
//       }
//     }
//     .contact {
//       background-color: #ffffff15;
//       min-height: 5rem;
//       cursor: pointer;
//       border-radius: 0.5rem;
//       display: flex;
//       align-items: center;
//       justify-content: center;
//       transition: 0.5s ease-in-out;
//       .avatar {
//         img {
//           height: 3rem;
//         }
//       }
//       .username {
//         h3 {
//           color: #e4e6eb;
//           display: none;
//         }
//       }

//       &:hover {
//         filter: brightness(80%);
//       }
//     }
//     .selected {
//       /* background-color: #9a86f3; */
//       background-color: rgba(45, 136, 255, 0.1);
//     }
//     @media screen and (min-width: 720px) {
//       .contact {
//         flex-direction: row;
//         justify-content: flex-start;

//         padding: 0.4rem;
//         gap: 1rem;
//         .username {
//           h3 {
//             color: white;
//             display: block;
//           }
//         }
//       }
//     }
//   }
//   .current-user {
//     background-color: #18191a;
//     display: flex;
//     justify-content: center;
//     align-items: center;
//     border-top: 0.2px solid #ffffff15;
//     .avatar {
//       height: 3.1rem;
//       position: relative;
//       img {
//         height: 3.1rem;
//         /* max-inline-size: 100%; */
//       }
//       .camera-img {
//         position: absolute;
//         left: 0;
//         top: 0;
//         background-color: #ffffff42;
//         border-radius: 50%;
//         height: 3.1rem;
//         width: 3.1rem;
//         display: flex;
//         align-items: center;
//         justify-content: center;
//         cursor: pointer;
//         img {
//           height: 2.5rem;
//           width: 2.5rem;
//         }
//       }
//     }
//     .username {
//       h2 {
//         color: white;
//         display: none;
//       }
//     }
//     @media screen and (min-width: 720px) {
//       gap: 1rem;
//       justify-content: flex-start;
//       padding: 0.4rem;

//       .username {
//         h2 {
//           font-size: 1rem;
//           display: block;
//           font-size: 1.2rem;
//         }
//       }
//     }
//   }
//   @media screen and (max-width: 900px) and (orientation: landscape) {
//     grid-template-rows: 15% 70% 15%;
//     .contacts {
//       .contact {
//         min-height: 4rem;
//       }
//     }
//     h3 {
//       display: none;
//     }
//   }
// `;

export default Contacts;
