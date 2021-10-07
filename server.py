from flask import Flask, render_template, request, redirect, session
from log_reg_app import app
from log_reg_app.controllers import users_controller

if __name__ == "__main__":
    app.run( debug = True )