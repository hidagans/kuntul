import os
import requests
import logging
from telegram.ext import Updater, CommandHandler
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Fungsi untuk menangani perintah /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Halo! Kirimkan link Google Drive untuk mendownload file.")

# Fungsi untuk mendownload file dari Google Drive
def download_from_drive(file_id, filename):
    # Inisialisasi Google Drive API
    drive_service = build('drive', 'v3')

    # Mendownload file
    request = drive_service.files().get_media(fileId=file_id)
    fh = open(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        logging.info("Download {}%.".format(int(status.progress() * 100)))
    fh.close()

# Fungsi untuk menangani perintah /download
def download(update, context):
    # Mendapatkan URL file dari pesan
    url = context.args[0]

    # Menentukan nama file
    filename = url.split('/')[-1]

    # Mendownload file dari Google Drive
    file_id = url.split('/')[-2]
    download_from_drive(file_id, filename)

    context.bot.send_message(chat_id=update.effective_chat.id, text="File berhasil diunduh.")

# Fungsi untuk mengunggah file ke Telegram
def upload_to_telegram(file_path, chat_id):
    context.bot.send_document(chat_id=chat_id, document=open(file_path, 'rb'))

# Fungsi untuk menangani perintah /upload
def upload(update, context):
    # Mendapatkan file yang dikirim oleh pengguna
    file = context.bot.get_file(update.message.document.file_id)

    # Menyimpan file dengan nama yang sama
    file_path = file.file_path.split('/')[-1]
    file.download(file_path)

    # Mengunggah file kembali ke Telegram
    upload_to_telegram(file_path, update.effective_chat.id)

    context.bot.send_message(chat_id=update.effective_chat.id, text="File berhasil diunggah.")

def main():
    # Token bot Telegram
    token = 'TOKEN_BOT_ANDA'

    # Membuat objek Updater
    updater = Updater(token=token, use_context=True)

    # Mendapatkan objek Dispatcher
    dispatcher = updater.dispatcher

    # Menambahkan handler untuk perintah /start
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # Menambahkan handler untuk perintah /download
    download_handler = CommandHandler('download', download)
    dispatcher.add_handler(download_handler)

    # Menambahkan handler untuk perintah /upload
    upload_handler = CommandHandler('upload', upload)
    dispatcher.add_handler(upload_handler)

    # Memulai bot
    updater.start_polling()

    # Menjaga bot berjalan sampai pengguna menghentikannya
    updater.idle()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
