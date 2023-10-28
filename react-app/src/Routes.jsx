import { Route, Routes as DomRoutes } from "react-router-dom";
import Home from "./pages/Home";
import Solve from "./pages/Solve";
import Result from "./pages/Result";

export default function Routes() {
    return (
        <DomRoutes>
            <Route path='/' element={<Home/>} />
            <Route path='/solve/:problem' element={<Solve/>}></Route>
            <Route path='/result' element={<Result/>}></Route>
        </DomRoutes>
    );
}