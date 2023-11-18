import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import axios from 'axios';
import { Alert } from '@mui/material';
import IconButton from '@mui/material/IconButton';
import Collapse from '@mui/material/Collapse';
import CloseIcon from '@mui/icons-material/Close';
import { useNavigate } from 'react-router-dom';
import { useCookies } from 'react-cookie';

function SignUp() {
    const database_url = 'http://127.0.0.1:7432'
    const [usernameExists, setUsernameExists] = React.useState(false);
    const [invalidPasswords, setInvalidPasswords] = React.useState(false);
    const [failed, setFailed] = React.useState(false);
    const [cookies, setCookie] = useCookies(['user'])
    const navigate = useNavigate();

    async function handleSubmit(event){
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    if (data.get('password') !== data.get('confirm')) {
        setInvalidPasswords(true)
    }

    else {

        const username = data.get('username');
        const password = data.get('password');

        const postData = {
            'username': username,
            'password': password,
            }
    
        try {
        
            const response = await axios.post(database_url + "/sign_up", postData);
            const result = response.data['sign_up_result']
        
            console.log(response)
            
            if (result == "Username already exists"){
                setUsernameExists(true);
        
            }
            
            else if (result == "Failed"){
                setFailed(true)
        
            }
        
            else if (result == "Success"){
                setCookie('username', username, { path: '/'})
                navigate('/')
            }

            else if (result == "Missing username or password in the request data"){
                console.log("Error: Missing username or password in the request data")

            }
        
            else {
                console.log("Error: Missing JSON obejct from server")
            }
    
        }

        catch {
            console.log("Error when retrieving authentication results")
        }
    }

    };

    return (
    // <ThemeProvider theme={defaultTheme}>
    <div>
        <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Collapse in={usernameExists}>
            <Alert
            severity='error'
            action={
                <IconButton
                aria-label="close"
                color="inherit"
                size="small"
                onClick={() => {
                    setUsernameExists(false);
                }}
                >
                <CloseIcon fontSize="inherit" />
                </IconButton>
            }
            sx={{ mb: 2 }}
            >
            Username Already Exists
            </Alert>
        </Collapse>
        <Collapse in={invalidPasswords}>
            <Alert
            severity='error'
            action={
                <IconButton
                aria-label="close"
                color="inherit"
                size="small"
                onClick={() => {
                    setInvalidPasswords(false);
                }}
                >
                <CloseIcon fontSize="inherit" />
                </IconButton>
            }
            sx={{ mb: 2 }}
            >
            Passwords don't match
            </Alert>
        </Collapse>
        <Collapse in={failed}>
            <Alert
            severity='error'
            action={
                <IconButton
                aria-label="close"
                color="inherit"
                size="small"
                onClick={() => {
                    setFailed(false);
                }}
                >
                <CloseIcon fontSize="inherit" />
                </IconButton>
            }
            sx={{ mb: 2 }}
            >
            Sign Up Failed
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
            Sign Up
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
            <TextField
                margin="normal"
                required
                fullWidth
                name="confirm"
                label="Confirm Password"
                type="confirm"
                id="confirm"
                autoComplete="confirm-password"
            />

            <Button
                type="submit"
                fullWidth
                variant="contained"
                sx={{ mt: 3, mb: 2 }}
            >
                Sign Up
            </Button>
            </Box>
        </Box>
        </Container>
    </div>
    );
    }

export default SignUp;