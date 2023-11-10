import { Route, Routes as DomRoutes } from "react-router-dom";
import Home from "./pages/Home";
import Solve from "./pages/Solve";
import Result from "./pages/Result";
import Leaderboard from "./pages/Leaderboard"

export default function Routes() {
    return (
        <DomRoutes>
            <Route path='/' element={<Home/>} />
            <Route path='/solve/:problem' element={<Solve/>}></Route>
            <Route path='/result' element={<Result/>}></Route>
            <Route path='/leaderboard' element={<Leaderboard/>}></Route>
        </DomRoutes>
    );
}