import React, { useState } from "react";
import { BrowserRouter, Route, Switch } from "react-router-dom";
import ScrollToTop from "./component/scrollToTop";

import { Home } from "./pages/home";
import { Example } from "./component/myChart";
import { BusinessDetails } from "./pages/businessDetails";
import { Prospects } from "./pages/prospects";
import injectContext, { Context } from "./store/appContext";
import { ProspectDetails } from "./pages/prospectDetails";
import { Landing } from "./pages/landing";

import { NavigationBar } from "./component/navbar";
import { Footer } from "./component/footer";
import { useContext } from "react";
import { useEffect } from "react";
import { Spinner, Container } from "react-bootstrap";
import { EditContact } from "./component/editContact";

//create your first component
const Layout = () => {
	//the basename is used when your project is published in a subdirectory and not in the root of the domain
	// you can set the basename on the .env file located at the root of this project, E.g: BASENAME=/react-hello-webapp/
	const basename = process.env.BASENAME || "";

	const { store, actions } = useContext(Context);

	return (
		<div className="d-flex flex-column h-100">
			<BrowserRouter basename={basename}>
				<ScrollToTop>
					<NavigationBar />
					<Switch>
						<Route exact path="/">
							<Landing />
						</Route>
						<Route exact path="/logged">
							<Home />
						</Route>
						<Route exact path="/businessDetails/:account">
							<BusinessDetails />
						</Route>
						<Route exact path="/editContact/:id/:prospect_id">
							<EditContact />
						</Route>
						<Route exact path="/prospectDetails/:prospect_id/:editContact">
							<ProspectDetails />
						</Route>
						<Route>
							<h1>Not found!</h1>
						</Route>
					</Switch>
					<Footer />
				</ScrollToTop>
			</BrowserRouter>
		</div>
	);
};

export default injectContext(Layout);
