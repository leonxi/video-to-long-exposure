# coding=utf-8
import streamlit as st
import cv2 as cv

class MyImgUtils():
    @staticmethod
    def averager():
        """Calculate the average using a clojure."""
        count = 0
        total = 0.0

        def averager(value):
            nonlocal count, total
            count += 1
            total += value
            return total / count

        return averager

    @staticmethod
    def maxer():
        """Calculate the max using a clojure."""
        maxium = 0.0

        def maxer(value):
            nonlocal maxium
            maxium = cv.max(maxium, value)
            return maxium

        return maxer

MyImgUtils.switch = {
    1: MyImgUtils.averager(),
    2: MyImgUtils.maxer()
}