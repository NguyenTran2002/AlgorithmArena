import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Typography from '@mui/material/Typography';
import { useCookies } from 'react-cookie';
import { Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';


function Settings() {
    const theme = createTheme();
    const [cookies, setCookie] = useCookies(['user'])
    const navigate = useNavigate()

    theme.typography.h3 = {
        fontSize: '1.2rem',
        '@media (min-width:600px)': {
            fontSize: '1.5rem',
        },
        [theme.breakpoints.up('md')]: {
            fontSize: '2.4rem',
        },
    };

    const handleSignout = () => {
        setCookie('username', null, { path: '/' });
        navigate('/');
    }

    const navigateHome = () => {
        navigate('/'); // Change this to the desired home route
    }

    return (
        <ThemeProvider theme={theme}>
            <Typography variant="h3">{cookies.username}</Typography>
            <Button onClick={handleSignout}>Sign Out</Button><br></br>
            <Button onClick={navigateHome}>Go Home</Button>
        </ThemeProvider>
    )
}


export default Settings;