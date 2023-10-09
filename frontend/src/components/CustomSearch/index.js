import { useState } from "react";
import {
  TextField,
  Container,
  InputAdornment,
  FormLabel,
  Box,
  Button
} from "@mui/material";
import { styled } from "@mui/material/styles";
import { useTranslation } from "react-i18next";
import { RiCloseCircleLine } from "react-icons/ri";
import { HiSearchCircle } from "react-icons/hi";

const StyleSearch = styled(TextField)`
  width: 90%;
  display: inline-flex;
  flex: 1;
  animation: fade-in 500ms forwards;
  &.hide-search {
    display: none;
  }
  .MuiInputLabel-root {
    &.Mui-focused {
      color: #ee0033;
    }
  }
  .MuiInputBase-root {
    border-radius: 6px;
    border: 1px solid grey;
    padding: 0;
    .MuiInputBase-input.MuiOutlinedInput-input {
      padding: 8px 12px;
      color: white;
    }
  }
  .Mui-focused .MuiOutlinedInput-notchedOutline {
    border-size: 1px !important;
    border-color: grey !important;
  }

  @keyframes fade-in {
    0% {
      opacity: 0;
      width: 0%;
      flex: 0;
    }
    100% {
      opacity: 1;
      width: 90%;
      flex: 1;
    }
  }
`;

const Label = styled(FormLabel)`
  font-size: var(--header-size-s);
  margin-bottom: 4px;
  font-family: var(--header-font-family);
`;

const SearchIcon = styled(HiSearchCircle)`
  width: 40px;
  height: 40px;
  color: grey;
  margin-right: 8px;
  cursor: pointer;
`;

const SearchButton = styled(Button)`
  height: 40px;
  line-height: 40px;
  width: 25%;
  cursor: pointer;
  background-color: grey;
  color: white;
  border-top-right-radius: 6px;
  border-bottom-right-radius: 6px;
  padding: 0 8px;
  text-transform: capitalize;

  &:hover {
    background-color: grey !important;
  }
`;

const CustomSearch = (props) => {
  const { label, direction } = props;
  const { t } = useTranslation();
  const [searchValue, setSearchValue] = useState("");
  const [isShow, setIsShow] = useState(true);

  const handleChange = (e) => {
    // if (!e.target.value && value) changeform("");
    setSearchValue(e.target.value);
  };

  const clearSearch = () => {
    setSearchValue("");
    // if (value) changeform("");
  };

  const SearchClear = styled(InputAdornment)`
    visibility: ${searchValue ? "visible" : "hidden"};
    display: ${searchValue ? "flex" : "none"};
    cursor: pointer;
    padding-left: 12px;
    margin-right: 0;
    color: grey;
    font-size: var(--header-size-l);
  `;

  return (
    <Container
      sx={{
        padding: "0 !important",
        display: props.row ? "flex" : "block",
        flexDirection: props.row ? "row" : "column",
      }}
    >
      <Box
        sx={{
          display: "flex",
          justifyContent: "flex-start",
          alignItems: "center",
          ...(direction === "right" && { flexDirection: "row-reverse" }),
        }}
      >
        {/* <SearchIcon /> */}
        <SearchIcon
          onClick={() => {
            setIsShow(!isShow);
            if (isShow) clearSearch();
          }}
        />
        <StyleSearch
          id="search"
          // type="search"
          // label="Search"
          className={!isShow ? "hide-search" : ""}
          placeholder={t("text.quickSearchByName")}
          value={searchValue}
          onChange={handleChange}
          onKeyDown={(e) => null
            // e.key === "Enter" &&
            // searchValue !== value &&
            // typeof changeform === "function" &&
            // changeform(searchValue)
          }
          InputProps={{
            startAdornment: (
              <SearchClear
                position="start"
                onClick={() => {
                  clearSearch();
                }}
              >
                <RiCloseCircleLine />
              </SearchClear>
            ),
            endAdornment: (
              <SearchButton
                onClick={() => null
                  // searchValue !== value &&
                  // typeof changeform === "function" &&
                  // changeform(searchValue)
                }
              >
                {t("btn.search")}
              </SearchButton>
            ),
          }}
          // {...rest}
        />
      </Box>
    </Container>
  );
};

export default CustomSearch;