import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Checkbox from '@mui/material/Checkbox';
// import Link from '@mui/material/Link';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import axios from 'axios';
import { Alert } from '@mui/material';
import IconButton from '@mui/material/IconButton';
import Collapse from '@mui/material/Collapse';
import CloseIcon from '@mui/icons-material/Close';
import { Link, useNavigate } from 'react-router-dom';
import { useCookies } from 'react-cookie';


// function Copyright(props) {
//   return (
//     <Typography variant="body2" color="text.secondary" align="center" {...props}>
//       {'Copyright © '}
//       <Link color="inherit" href="https://mui.com/">
//         AlgorithmArena.com
//       </Link>{' '}
//       {new Date().getFullYear()}
//       {'.'}
//     </Typography>
//   );
// }

// TODO remove, this demo shouldn't need to reset the theme.

// const defaultTheme = createTheme();

function Login() {
  const database_url = 'http://127.0.0.1:7432'
  const [invalidUsername, setInvalidUsername] = React.useState(false);
  const [invalidPassword, setInvalidPassword] = React.useState(false);
  const [cookies, setCookie] = useCookies(['user'])
  const navigate = useNavigate();

  async function handleSubmit(event){
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    username = data.get('username')
    password = data.get('password')

    const postData = {
      'username': username,
      'password': password,
    }

    try {

      const response = await axios.post(database_url + "/authenticate", postData);
      const result = response.data['authentication_result']

      console.log(response)
      
      if (result == "Username Doesn't Exist"){
        setInvalidUsername(true);

      }
      
      else if (result == "Incorrect Password"){
        setInvalidPassword(true)

      }

      else if (result == "Success"){
        setCookie('username', username, { path: '/'})
        // setCookie('password', password, { path: '/'})
        navigate('/');

      }

      else {
        console.log("Error when retrieving authentication results: no json passed from server-side")
      }

    }
    catch{
      console.log("Error when retrieving authentication results")
    }

  };

  return (
    // <ThemeProvider theme={defaultTheme}>
    <div>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Collapse in={invalidUsername}>
          <Alert
            severity='error'
            action={
              <IconButton
                aria-label="close"
                color="inherit"
                size="small"
                onClick={() => {
                  setInvalidUsername(false);
                }}
              >
                <CloseIcon fontSize="inherit" />
              </IconButton>
            }
            sx={{ mb: 2 }}
          >
            Invalid Username
          </Alert>
        </Collapse>
        <Collapse in={invalidPassword}>
          <Alert
            severity='error'
            action={
              <IconButton
                aria-label="close"
                color="inherit"
                size="small"
                onClick={() => {
                  setInvalidPassword(false);
                }}
              >
                <CloseIcon fontSize="inherit" />
              </IconButton>
            }
            sx={{ mb: 2 }}
          >
            Invalid Password
          </Alert>
        </Collapse>
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign in
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            {/* <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            /> */}
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
            <Grid item>
                <Link href="#" variant="body2" to="/SignUp">
                  {"Don't have an account? Sign Up"}
                </Link>
            </Grid>
            {/* <Grid container>
              <Grid item xs>
                <Link href="#" variant="body2">
                  Forgot password?
                </Link>
              </Grid>
              <Grid item>
                <Link href="#" variant="body2" to="/SignUp">
                  {"Don't have an account? Sign Up"}
                </Link>
              </Grid>
            </Grid> */}
          </Box>
        </Box>
        {/* <Copyright sx={{ mt: 8, mb: 4 }} /> */}
      </Container>
    </div>
    // </ThemeProvider>
  );
}

export default Login;