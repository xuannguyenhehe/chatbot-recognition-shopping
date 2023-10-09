import { Box } from "@mui/material";

const Footer = () => {
  return (
    <Box
      sx={{
        width: "100%",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        borderTop: "1px solid black",
        py: "10px",
        height: '30px',
        color: "white",
      }}
    >
      &copy; Copyright Automation Chatbot
    </Box>
  );
};

export default Footer;
