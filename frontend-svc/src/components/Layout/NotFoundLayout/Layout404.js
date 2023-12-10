import { Box, Grid, Typography } from "@mui/material";
import { FiChevronsLeft } from "react-icons/fi";
import { useTranslation } from "react-i18next";
import notFoundImg from 'assets/notfound.png';
import Button from "react-bootstrap/Button";

function Layout404() {
  const { t } = useTranslation();

  return (
    <Box className="text-center" sx={{height: "calc(100vh - var(--header-height))"}}>
      <Grid
        container
        justifyContent={'center'}
        height='100%'
        flexDirection={'column'}
        alignItems={'center'}
      >
        <Typography fontSize='4.5rem' fontWeight={'bold'} fontFamily='Magistral'>404 ERROR!</Typography>
        <Typography component='img' src={notFoundImg} alt={''} width='40%'/>
        <Button
          sx={{
            marginTop: "20px",
            marginLeft: "20px",
          }}
          colorIcon={"white"}
          icon={<FiChevronsLeft />}
          onClick={() => window.history.back()}
        >{t("btn.back")}</Button>
      </Grid>
    </Box>
  );
}

export default Layout404;
