import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

keyboard_start = VkKeyboard(one_time=False)
keyboard_start.add_button('⚙️', color=VkKeyboardColor.PRIMARY)
keyboard_start.add_button('ℹ️', color=VkKeyboardColor.PRIMARY)
keyboard_start.add_button('Таймеры', color=VkKeyboardColor.PRIMARY)
keyboard_start.add_button('Дикси', color=VkKeyboardColor.PRIMARY)
#keyboard_start.add_line()
#keyboard_start.add_button('Чат', color=VkKeyboardColor.PRIMARY)

keyboard_admin_menu = VkKeyboard(one_time=False)
keyboard_admin_menu.add_button('Рассылка',color=VkKeyboardColor.PRIMARY)
keyboard_admin_menu.add_button('Назад',color=VkKeyboardColor.PRIMARY)

keyboard_start_admin = VkKeyboard(one_time=False)
keyboard_start_admin.add_button('⚙️', color=VkKeyboardColor.PRIMARY)
keyboard_start_admin.add_button('ℹ️', color=VkKeyboardColor.PRIMARY)
keyboard_start_admin.add_button('Таймеры', color=VkKeyboardColor.PRIMARY)
keyboard_start_admin.add_line()
#keyboard_start_admin.add_button('Чат', color=VkKeyboardColor.PRIMARY)
keyboard_start_admin.add_button('Дикси', color=VkKeyboardColor.PRIMARY)
keyboard_start_admin.add_button('Админ', color=VkKeyboardColor.PRIMARY)

keyboard_info = VkKeyboard(one_time=True)
keyboard_info.add_button('Деканаты', color=VkKeyboardColor.PRIMARY)
keyboard_info.add_button('ЖКО', color=VkKeyboardColor.PRIMARY)
keyboard_info.add_button('Администрация', color=VkKeyboardColor.PRIMARY)
keyboard_info.add_line()
keyboard_info.add_button('Правила', color=VkKeyboardColor.PRIMARY)
keyboard_info.add_button('Услуги', color=VkKeyboardColor.PRIMARY)
keyboard_info.add_button('Назад', color=VkKeyboardColor.PRIMARY)

keyboard_timers = VkKeyboard(one_time=False)
keyboard_timers.add_button('Стирка', color=VkKeyboardColor.PRIMARY)
keyboard_timers.add_button('Сушка', color=VkKeyboardColor.PRIMARY)
keyboard_timers.add_button('Назад', color=VkKeyboardColor.PRIMARY)

keyboard_stirka = VkKeyboard(one_time=False)
keyboard_stirka.add_button('Занять', color=VkKeyboardColor.PRIMARY)
keyboard_stirka.add_button('Сообщить', color=VkKeyboardColor.PRIMARY)
keyboard_stirka.add_line()
keyboard_stirka.add_button("Освободить",color=VkKeyboardColor.PRIMARY)
keyboard_stirka.add_button('Назад', color=VkKeyboardColor.PRIMARY)

keyboard_spam=VkKeyboard(one_time=False)
keyboard_spam.add_button("Бельё")
keyboard_spam.add_button("Массовая")

keyboard_suhka=VkKeyboard(one_time=False, inline=True)
keyboard_suhka.add_button(label='обновить таймер', color=VkKeyboardColor.PRIMARY)
keyboard_suhka.add_line()
keyboard_suhka.add_button(label='Нет, я всё забрал/забралa', color=VkKeyboardColor.POSITIVE)

keyboard_podpiski=VkKeyboard(inline=True)
keyboard_podpiski.add_button('Заполнить',VkKeyboardColor.PRIMARY)

keyboard_DIXI_status=VkKeyboard(one_time=True)
keyboard_DIXI_status.add_button("Открыто")
keyboard_DIXI_status.add_button("Закрыто")

keyboard_DIXI=VkKeyboard(inline=True)
keyboard_DIXI.add_button('Изменить состояние',VkKeyboardColor.PRIMARY)


keyboard_da_net=VkKeyboard(inline=True)
keyboard_da_net.add_button("Да", color=VkKeyboardColor.PRIMARY)
keyboard_da_net.add_button("Нет", color=VkKeyboardColor.NEGATIVE)


keyboard_choice_washmashine = VkKeyboard(one_time=False)
keyboard_choice_washmashine.add_button("1", color=VkKeyboardColor.PRIMARY)
keyboard_choice_washmashine.add_button("2", color=VkKeyboardColor.PRIMARY)
keyboard_choice_washmashine.add_button("3", color=VkKeyboardColor.PRIMARY)
keyboard_choice_washmashine.add_button("4", color=VkKeyboardColor.PRIMARY)
keyboard_choice_washmashine.add_button("Назад", color=VkKeyboardColor.PRIMARY)