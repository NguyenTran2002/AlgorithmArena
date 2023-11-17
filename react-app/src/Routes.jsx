import { Route, Routes as DomRoutes } from "react-router-dom";
import Home from "./pages/Home";
import Solve from "./pages/Solve";
import Result from "./pages/Result";
import Leaderboard from "./pages/Leaderboard";
import Login from "./pages/login";
import SignUp from "./pages/Signup";
import Settings from "./pages/Settings";


export default function Routes() {
    return (
        <DomRoutes>
            <Route path='/SignUp' element={<SignUp></SignUp>}/>
            <Route path='/Login' element={<Login></Login>}/>
            <Route path='/' element={<Home/>} />
            <Route path='/solve/:problem' element={<Solve/>}></Route>
            <Route path='/result' element={<Result/>}></Route>
            <Route path='/leaderboard' element={<Leaderboard/>}></Route>
            <Route path='/settings' element={<Settings/>}></Route>
        </DomRoutes>
    );
}