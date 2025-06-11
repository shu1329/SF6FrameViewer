import flet as ft
from frame import chara, frame
from character_class import Character, Process

def main(page: ft.Page):
    title_name = "Frame Data Viewer -ver.ELENA"
    update_date = "2025/6/11"
    update_version = "2.4.6"
    page.title = title_name
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.bgcolor="#FFFFFF"
    page.scroll=ft.ScrollMode.AUTO
    # ウィンドウサイズの設定
    page.window_height = 800
    page.window_width = 400

    title_text = ft.Text(value=title_name, theme_style=ft.TextThemeStyle.TITLE_MEDIUM)
    
    attention_button = ft.IconButton(icon=ft.icons.ANNOUNCEMENT_ROUNDED, icon_size=20, on_click=lambda e: open_dlg(e))
    
    title = ft.Container(
        ft.Row(
            [title_text, attention_button], 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
    )
    # キャラクター選択用のドロップダウンリスト
    my_character_dropdown = ft.Dropdown(
        label="自分のキャラ",
        width=700,
        bgcolor="#FFFFFF",
        options=[ft.dropdown.Option(str(i), chara[i]) for i in range(len(chara))],
        on_change=lambda e: populate_moves()
    )

    op_character_dropdown = ft.Dropdown(
        label="相手のキャラ",
        width=700,
        bgcolor="#FFFFFF",
        options=[ft.dropdown.Option(str(i), chara[i]) for i in range(len(chara))],
        on_change=lambda e: populate_moves()
    )

    # パニカンできる技一覧
    move_dropdown = ft.Dropdown(
        label="相手が振る技",
        width=700,
        bgcolor="#FFFFFF",
        options=[],
        on_change=lambda e: show_counters()
    )

    # 表示用
    text = ft.Text(value="")
    text.visible = False

    nomal_text = ft.Text(value="通常技", visible=False)

    nomal_counter_list_view = ft.ListView(height=120, width=700, spacing=10, padding=ft.padding.only(left=20))

    special_text = ft.Text(value="タゲコン・必殺技", visible=False)

    special_counter_list_view = ft.ListView(height=120, width=700, spacing=10, padding=ft.padding.only(left=20))

    rush_switch = ft.CupertinoSwitch(
        value=True,
        on_change=lambda e: toggle_button(e)
    )

    rush = ft.Container(
        content=ft.Row([
            ft.Text("ラッシュを含む"),
            rush_switch
        ], 
        alignment=ft.MainAxisAlignment.END,
        ),
        visible=False
    )

    # バーンアウト時スイッチ
    bo_switch = ft.CupertinoSwitch(
        value=False,
        on_change=lambda e: toggle_button(e),
    )

    all_move_switch = ft.CupertinoSwitch(
        value=False,
        on_change=lambda e: toggle_button(e)
    )

    burn = ft.Container(
        content=ft.Row(
            [ft.Text("バーンアウト"), bo_switch,],
            alignment=ft.MainAxisAlignment.END,
        ),
    )

    alls = ft.Container(
        content=ft.Row([ft.Text("全ての技を表示"), all_move_switch], alignment=ft.MainAxisAlignment.END),
    )

    swithes = ft.Container(
        content=ft.Row([burn, alls, rush], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        width=700,
    )

    tb = ft.TextField(label="発生フレーム", width=180)
    sub = ft.ElevatedButton(text="探す", on_click=lambda e: populate_moves())
    textbox = ft.Container(content=ft.Row([tb, sub]), visible=False)
    date_text = ft.Text(value="latest update: " + update_date, size=10)
    version_text = ft.Text(value="ver" + update_version, size=10)
    update_row = ft.Row([date_text, version_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)

 
    cnt2 = ft.Container(content=ft.Column([
        my_character_dropdown,
        op_character_dropdown,
        move_dropdown,
        swithes,
        textbox,
        text,
        nomal_text,
        nomal_counter_list_view,
        special_text,
        special_counter_list_view,
        ft.Divider(height=3),
        update_row
    ]))

    cm = ft.Container(
        content=ft.Text("反撃できる技検索", color=ft.colors.BLUE_ACCENT_400, theme_style=ft.TextThemeStyle.TITLE_SMALL, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
        padding=15,
        border=ft.border.only(bottom=ft.border.BorderSide(3, ft.colors.INDIGO)),
        on_hover=lambda e: on_hover(e),
        on_click=lambda e: cnt_click(e, fa, sch, 0),
        alignment=ft.alignment.center,
        expand=True
        )
    
    fa = ft.Container(
        content=ft.Text("ガードで有利な技", theme_style=ft.TextThemeStyle.TITLE_SMALL, max_lines=1, overflow=ft.TextOverflow.ELLIPSIS),
        padding=15,
        on_hover=lambda e: on_hover(e),
        on_click=lambda e: cnt_click(e, cm, sch, 1),
        alignment=ft.alignment.center,
        expand=True
    )

    sch = ft.Container(
        content=ft.Icon(name=ft.icons.SEARCH, size=30),
        padding=10,
        on_hover=lambda e: on_hover(e),
        on_click=lambda e: cnt_click(e, cm, fa, 2)
    )

    cnt = ft.Container(
        content=ft.Row([cm, fa, sch], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        # bgcolor=ft.colors.YELLOW,
        width=700,
        )
    
    dlg = ft.AlertDialog(
        title=ft.Text("このシステムにおいて、技のリーチなどは考慮に入れていないため、実際には確反が届かない場合があります",
        size=16,
        ),
        shape=ft.BeveledRectangleBorder(radius=5)
    )
    
    body = ft.Container(
        content=ft.Column([
            title,
            ft.Divider(height=1),
            cnt,
            ft.Divider(height=1),
            cnt2
        ]),
        width=700,
    )

    num = 0
    
    def populate_moves():
        if (num == 0 and (not my_character_dropdown.value or not op_character_dropdown.value)) or (num == 1 and not my_character_dropdown.value) or (num == 2 and not my_character_dropdown.value):
                return
        
        # ドロップダウンリストをクリア
        text.visible = False
        move_dropdown.options = []
        nomal_counter_list_view.controls.clear()
        special_counter_list_view.controls.clear()
        global my, op
        my = Character(frame[int(my_character_dropdown.value)])
        

        if num == 0:
            op = Character(frame[int(op_character_dropdown.value)])
            moves = op.counterable(bo_switch.value, all_move_switch.value)
            for i in range(len(moves)):
                move_text = f'{moves[i][0]}({moves[i][2]+4})' if bo_switch.value else f'{moves[i][0]}({moves[i][2]})'
                move_dropdown.options.append(ft.dropdown.Option(str(i), move_text))
                move_dropdown.update()
        elif num == 1:
            nomal, spetial = my.advantage(rush_switch.value, bo_switch.value)
            nomal_counter_list_view.controls = nomal
            special_counter_list_view.controls = spetial
        else:
            term = True
            try:
                maf = int(tb.value)
            except:
                term = False
                text.value = "整数で発生フレームを入れてください"
                text.visible = True

            if term:
                if maf < 0:
                    maf = -maf
                nomal, spetial = my.search_counters(maf, 2)
                text.value= f"{maf}Fで発生する技は見つかりませんでした" if not nomal and not spetial else f"{maf}Fで発生する技:"
                text.visible = True

                nomal_counter_list_view.controls = nomal
                special_counter_list_view.controls = spetial
        page.update()


    def show_counters():
        if not move_dropdown.value or num != 0:
            return
        nomal_text.visible = True
        special_text.visible = True
        nomal_counter_list_view.controls.clear()
        special_counter_list_view.controls.clear()
        selected_index = int(move_dropdown.value)

        p = Process(my, op)
        nomal, spetial = p.show_counters(bo_switch.value, selected_index)

        if not nomal and not spetial:
            text.value = "反撃可能な技は見つかりませんでした"
        else:
            if bo_switch.value:
                text.value = f'{op.counterable_move[selected_index][0]}({op.counterable_move[selected_index][2]+4})に反撃可能な技:'
            else:
                text.value = f'{op.counterable_move[selected_index][0]}({op.counterable_move[selected_index][2]})に反撃可能な技:'
        text.visible = True

        nomal_counter_list_view.controls = nomal
        special_counter_list_view.controls = spetial
        page.update()

    def toggle_button(e):
        text.visible = False
        populate_moves()
        show_counters()
        page.update()

    def on_hover(e):
        e.control.bgcolor = ft.colors.BLUE_50 if e.data == "true" else ft
        e.control.update()
        
    def open_dlg(e):
        e.control.page.overlay.append(dlg)
        dlg.open = True
        e.control.page.update()

    def cnt_click(e, cnt1 :ft.Container, cnt2 :ft.Container, index :int):
        nonlocal num
        num = index
        e.control.border = ft.border.only(bottom=ft.border.BorderSide(3, ft.colors.INDIGO))
        cnt1.border = ft.border.only(bottom=ft.border.BorderSide(0, ft.colors.WHITE))
        cnt2.border = ft.border.only(bottom=ft.border.BorderSide(0, ft.colors.WHITE))
        e.control.content.color = ft.colors.BLUE_ACCENT_400
        cnt1.content.color = ft
        cnt2.content.color = ft
        e.control.update()
        cnt.update()
        nomal_counter_list_view.controls.clear()
        special_counter_list_view.controls.clear()

        if index == 0:  
            op_character_dropdown.visible = True
            burn.visible = True
            alls.visible = True
            rush.visible = False
            move_dropdown.visible = True
            text.visible = False
            nomal_text.visible = False
            special_text.visible = False
            textbox.visible = False
            populate_moves()
            show_counters()
            page.update()

        elif index == 1:
            op_character_dropdown.visible = False
            burn.visible = True
            alls.visible = False
            rush.visible = True
            move_dropdown.visible = False
            text.visible = False
            nomal_text.visible = True
            special_text.visible = True
            textbox.visible = False
            populate_moves()
            page.update()
        
        else:
            op_character_dropdown.visible = False
            burn.visible = False
            alls.visible = False
            rush.visible = False
            move_dropdown.visible = False
            text.visible = False
            nomal_text.visible = True
            special_text.visible = True
            textbox.visible = True
            populate_moves()
            page.update()


    page.add(body)

if __name__ == "__main__":
    ft.app(target=main)