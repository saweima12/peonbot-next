MEDIA_CHECKED="""
該圖檔已登錄，當前設置的關鍵字：{keywords}  
---  
可用指令：(關鍵字必須用逗號隔開如：/sk 低頭,廢鐵)
/sk - 設置圖檔的關鍵字，會覆蓋當前的所有關鍵字設定。
/ak - 新增圖檔的關鍵字。
"""
MEDIA_UNCHECKED="""
該圖檔已登錄，但尚未設定關鍵字。  
---  
可用指令：(關鍵字必須用逗號隔開如：/sk 低頭,廢鐵)
/sk - 設置圖檔的關鍵字，會覆蓋當前的所有關鍵字設定。
/ak - 新增圖檔的關鍵字。
"""

MEDIA_NEW="""
該圖檔尚未登錄，將會進行快取，可繼續進行操作。  
---
可用指令：(關鍵字必須用逗號隔開如：/sk 低頭,廢鐵)
/sk - 設置圖檔的關鍵字，會覆蓋當前的所有關鍵字設定。
/ak - 新增圖檔的關鍵字。
"""

HELP_MSG="""
*使用方式*
- 傳送一張貼圖或是 GIF 可以取得當前登錄的關鍵字及狀態。
- Reply 一張貼圖或是 GIF 並輸入 /ak 可增加該圖檔的關鍵字。
- Reply 一張貼圖或是 GIF 並輸入 /sk 可置重新設置該圖檔的關鍵字（覆蓋原有設置）

*注意事項*
- 關鍵字必須用半形逗號,隔開中間不可有其他的空白。
- 關鍵字添加後會由資料庫處理索引，需要幾分鐘的時間。
"""

REGISTER_SUCCESS="註冊成功！"

MSG_500 = "遇到未知錯誤，請聯繫此機器的管理者。"

SK_NEED_REPLY="需要 reply 一個貼圖或是 GIF。"
SK_PRAMAS_ERROR="關鍵字必須至少有一組並且用半形逗號隔開。"
SK_404_DOCUMENT="找不到對應的貼圖或是 GIF, 請重新登錄。"

SK_SUCCESS="設置關鍵字成功。新的關鍵字組為：{keywords}"
AK_SUCCESS="新增關鍵字成功。新的關鍵字組為：{keywords}"
RM_SUCCESS="移除 Media 成功。"