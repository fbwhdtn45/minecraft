from ursina import *

class Inventory(Button):
    def __init__(self):
        # 초기 설정 ( 1 x 9 칸 )
        super().__init__(
            parent = camera.ui,
            model = 'quad',
            scale = (.9, .5),
            origin = (-.5,.5),                                          
            position = (-.5,.3),                                 
            color = color.black50,
            disabled = True                                     
            )

        # ㅡㅡㅡㅡㅡ 인벤토리 ㅡㅡㅡㅡㅡㅡ
        # Inventory 배경화면
        self.innventory_background = Button(parent=self, model = 'quad',scale = (.95,.65),origin = (-.5,.5),position = (.025,-.125,-.5), color = color.white10, disabled = True)
        # Invetory 제목
        self.title = Button(parent=self, model = 'quad',scale = (.95,.1),origin = (-.5,.5),position = (.025,-.025,-.5), color = color.black10, text = 'Inventory', disabled = True)

        # ( 5 x 9 )칸의 각 칸마다 자식 Entity 설정
        self.item_slot = Button(parent=self.innventory_background, modle = 'quad',scale=(1/9,1/5), color = color.clear,texture_scale = (9,5))       

        # ㅡㅡㅡㅡㅡㅡ 인벤토리 퀵 슬롯 ㅡㅡㅡㅡㅡㅡ
        # inventory_quick_slot slot 배경
        self.quick_background = Button(parent=self, model = 'quad',scale = (.95,.15),origin = (-.5,.5),position = (.025,-.8125,-.5), color = color.black50, disabled = True)

        # quick slot (1 x 9)칸의 각 칸마다 자식 entity 설정
        self.quick_slot = Button(parent = self.quick_background, model = 'quad', scale = (1/9,1), color = color.clear,texture_scale = (1,9))
        
        # ㅡㅡㅡㅡㅡ 인벤토리 퀵 슬롯 인덱스 ㅡㅡㅡㅡㅡ
        # quick index 배경
        self.quick_index_background = Button(parent=self, model = 'quad',scale = (.95,.03),origin = (-.5,.5),position = (.025,-.78,-.6), color = color.clear, disabled = True)

        # quick index 컴포넌트
        self.quick_index_slot = Button(parent = self.quick_index_background, model = 'quad', scale = (1/9,1), color = color.clear,texture_scale = (1,9))

        # 현재 visible 상태
        self.is_visibled = False

        self.is_first = True

        # 인벤토리 퀵 슬롯 인덱스 추가
        self.putIndex(self.quick_index_slot)

    def append(self,parent, texture, **kwargs):
        # 아이템 추가하려는데 빈 칸이 없는 경우, 추가하지 않음        
        pos = self.find_free_spot(parent)
        if not pos :
            return False
        
        # 아이템 추가 될 x,y좌표 주는 경우
        for key, value in kwargs.items() :
            if 'position' in kwargs.keys() :
                pos = value
        
        # 아이템 박스                                  
        item = Draggable(                                                         
            parent = parent,
            texture = texture,
            origin = (-.5,.5),
            icon = texture,
            position = pos                                                           
            )

        # 드래그 후, 놓았을 때
        def drop() :
            item.x = round(item.x,0)
            item.y = round(item.y,0)
            item.z += .01

            # 인벤토리 아이템에 대하여
            if item.parent == self.item_slot : 
                # 아이템이 인벤토리 바깥으로 나가지 못 하도록 함
                if item.x < 0 or item.x > 8 or item.y > 0 or item.y < -4: 
                    item.position = (item.org_pos)                        
                    return
            
                 # SWAP 하려는 아이템이 인벤토리 창에 있을 때,
                for e in self.item_slot.children :
                    if e != item :
                        if e.x == item.x and e.y == item.y :
                            item.position = e.position
                            e.position = item.org_pos

            # 퀵슬롯 아이템에 대하여
            if item.parent == self.quick_slot : 
                # 아이템이 인벤토리 바깥으로 나가지 못 하도록 함
                if item.x < 0 or item.x > 8 or item.y > 0 or item.y < 0: 
                    item.position = (item.org_pos)                        
                    return            
                # SWAP 하려는 아이템이 퀵슬롯 창에 있을 때,
                if item.parent == self.quick_slot : 
                    for e in self.quick_slot.children :
                        if e != item :
                            if e.x == item.x and e.y == item.y :
                                item.position = e.position
                                e.position = item.org_pos

        # 우클릭 시
        def rightclick() :
            # 인벤토리 아이템이면,
            if item.parent == self.item_slot :
                # 해당 칸 텍스쳐 지우고, 퀵슬롯 append
                if self.append(self.quick_slot,item.texture) :
                    destroy(item)
            
            # 퀵슬롯 아이템이면,
            if item.parent == self.quick_slot :
                # 해당 칸 텍스쳐 지우고, 인벤토리 append
                if self.append(self.item_slot,item.texture) :
                    destroy(item)

        # 아이템 드래그 클릭 했을 때
        def drag() :
            item.org_pos = (int(item.x), int(item.y),-.1)
            item.z -= -.01

        # 드래그 함수 바인딩
        item.drag = drag

        # 드롭 함수 바인딩
        item.drop = drop

        # 우클릭 함수 바인딩 ( 기존 Draggable 클래스 수정하였음 )
        item.rightClick = rightclick
        
        return True
    
    # 퀵슬롯 1 ~ 9 인덱스 추가
    def putIndex(self,parent) :
        for i in range(9) :
            # 각 박스 인덱스 설정
            Button(                                                         
                parent = parent,                             
                model = 'quad',
                scale = (1/5,1),    
                origin = (-.5,.5),                                    
                color = color.black33,
                text = str(i+1),
                position = (i,-1.2,-.1),                      
                z = -.3                                                     
                ) 

    # ( 1 x 9 ) 박스의 빈 칸 찾는 매서드
    def find_free_spot(self, item):                                                      
        taken_spots = [(int(e.x), int(e.y)) for e in item.children]
        
        # 인벤토리 아이템이면 5x9 에서 찾고
        if item == self.item_slot :
            temp = 5
        # 퀵슬롯 아이템이면 1x9 에서 찾는다.
        else : 
            temp = 1

        # 빈 칸 찾기
        for y in range(temp):                                                         
            for x in range(9):                                                     
                if not (x,-y) in taken_spots:                                      
                    return (x,-y,-.1)

        # 빈 칸이 없으면 원래 위치 반환
        return False

if __name__ == '__main__':
    app = Ursina()

    inventory = Inventory()
    
    app.run()
