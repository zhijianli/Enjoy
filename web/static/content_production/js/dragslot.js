;(function($, window, document, undefined){
	var eStart  = 'mousedown',
	eMove   = 'mousemove',
	eEnd    = 'mouseup';
	
	var clientX,clientY;
	var defaults = {
		slotItemClass : 'slot-item',
		placeholderClass : 'placeholder',
		dragItemClass : 'drag-item',
		slotListClass : 'slot-list',
		slotHandlerClass : 'slot-handler',
		emptySlotClass : 'empty-slot',
		slotClass : 'slot',
		slotItem : 'li',
		slotList : 'ul',
		dropCallback : null
 	}

    /**
     * 将秒转换为 分:秒
     * s int 秒数
    */
    function s_to_hs(s){
        //计算分钟
        //算法：将秒数除以60，然后下舍入，既得到分钟数
        var h;
        h  =   Math.floor(s/60);
        //计算秒
        //算法：取得秒%60的余数，既得到秒数
        s  =   s%60;
        //将变量转换为字符串
        h    +=    '';
        s    +=    '';
        //如果只有一位数，前面增加一个0
        h  =   (h.length==1)?'0'+h:h;
        s  =   (s.length==1)?'0'+s:s;
        h  =   Math.round(h)
        s  =   Math.round(s)
        return h+'分'+s+'秒';
    }
	
	function Dragslot(element,options){
		this.element = $(element);
		this.options = $.extend({}, defaults, options);
		return this.init();
	}
	Dragslot.prototype = {
		init : function(){
			var slotContainer = this;
			slotContainer.placeholder = $('<div class="'+ slotContainer.options.placeholderClass +'"/>');
			var dragStartEvent = function(e){
				var item = $(e.target);
				if(!item.closest('.' + slotContainer.options.slotItemClass)){
					return;
				}

				e.preventDefault();
				slotContainer._dragStart(e);

			};
			var dragMoveEvent = function(e){
				if(slotContainer.dragElement){
						e.preventDefault();
						slotContainer._dragMove(e);
					}
			};
			var dragEndEvent = function(e){
				if(slotContainer.dragElement){
						e.preventDefault();
						slotContainer._dragEnd(e,dragStartEvent,slotContainer);
					}

			};
			slotContainer.element.on(eStart, dragStartEvent);
			$(window).on(eMove, dragMoveEvent);
			$(window).on(eEnd, dragEndEvent);

            return{
              slotContainer:slotContainer,
              dragStartEvent:dragStartEvent
            }

		},
		_dragStart : function(e){
			var target = $(e.target),
			 dragItem = target.closest('.' + this.options.slotItemClass);
			this.placeholder.css('height', dragItem.height());
			this.dragElement = $(document.createElement('div')).addClass(this.options.dragItemClass);
			this.slotlist = target.closest('.' + this.options.slotListClass);
			dragItem.after(this.placeholder);
			dragItem.css('width',dragItem.width() + 'px');
			if(dragItem[0].parentNode){
				dragItem[0].parentNode.removeChild(dragItem[0]);
			}
			dragItem.appendTo(this.dragElement);
			$(document.body).append(this.dragElement);
			clientX = e.clientX + (document.body.scrollLeft || document.documentElement.scrollLeft);
			clientY = e.clientY + (document.body.scrollTop || document.documentElement.scrollTop);
			this.dragElement.css({
				'left' : clientX,
				'top'  : clientY
			});
		},
		_dragMove : function(e){
			var newClientX = e.clientX + (document.body.scrollLeft || document.documentElement.scrollLeft),
			newClientY = e.clientY + (document.body.scrollTop || document.documentElement.scrollTop);
			var left = parseInt(this.dragElement[0].style.left) || 0;
			var top = parseInt(this.dragElement[0].style.top) || 0;
			this.dragElement[0].style.left = left + (newClientX - clientX) + 'px';
			this.dragElement[0].style.top = top + (newClientY - clientY) + 'px';
			clientX = newClientX;
			clientY = newClientY;

            this.dragElement[0].style.visibility = 'hidden';
			this.pointEl = $(document.elementFromPoint(e.pageX - (document.body.scrollLeft || document.documentElement.scrollLeft), e.pageY - (document.body.scrollTop || document.documentElement.scrollTop)));

            this.dragElement[0].style.visibility = 'visible';

			if (this.pointEl.closest('.' + this.options.slotHandlerClass).length || this.pointEl.closest('.' + this.options.slotItemClass).length) {
                this.pointEl = this.pointEl.closest('.' + this.options.slotItemClass);
                 var before = e.pageY < (this.pointEl.offset().top + this.pointEl.height() / 2);
                    parent = this.placeholder.parent();

                if (before) {
                    this.pointEl.before(this.placeholder);
                }
                else {
                    this.pointEl.after(this.placeholder);
                }
            } else if (this.pointEl.hasClass(this.options.emptySlotClass)) {
                    list = $(document.createElement(this.options.slotList)).addClass(this.options.slotListClass);
                    list.append(this.placeholder);
                    this.pointEl.append(list);
                }else if(this.pointEl.hasClass(this.options.slotClass)){
            		this.pointEl = this.pointEl.children(this.options.slotList).children().last();
            		this.pointEl.after(this.placeholder);
            } else {
                return;
            }
            this.toSlot = this.pointEl.closest('.' + this.options.slotClass);
		},
		_dragEnd : function(e,dragStartEvent,slotContainer){
			var self = this;
			var el = self.dragElement.children('.' + self.options.slotItemClass).first();
            el[0].parentNode.removeChild(el[0]);
            this.placeholder.replaceWith(el);

            self.dragElement.remove();
            if($.isFunction(self.options.dropCallback)) {
              var itemInfo = {
              	dragItem : el,
              	sourceSlot : self.slotlist.closest('.slot'),
              	destinationSlot : self.toSlot,
              	dragItemId : el.attr('id')
              }
              self.options.dropCallback.call(self, itemInfo);
            }
            self.dragElement = null;
            self.pointEl = null;
            if (self.toSlot.hasClass(self.options.emptySlotClass)) {
                self.toSlot.removeClass(self.options.emptySlotClass);
            }
            if(self.slotlist.children().length==0){
            	self.slotlist.closest('.' + self.options.slotClass).addClass(self.options.emptySlotClass);
            	self.slotlist[0].parentNode.removeChild(self.slotlist[0]);
            }

           　//计算文字的总时长
            textList = document.getElementById("border-green").getElementsByClassName("item-title")
            timeLength = 0
            for (let i = 1; i < textList.length; ++i) {
//                textList[i].setAttribute('contentEditable', 'true');

                sentence = textList[i].innerText
//                sentence=sentence.replace(/\n/g,"")
//                console.log(parseInt(sentence.length/2.5))
                duration = parseInt(sentence.length/3)
                if(duration > 15){
                    duration = 15
                }
                timeLength = timeLength + duration
            }
            timeLength = s_to_hs(timeLength + 5)  //结尾这边有5秒钟时间，所以最后要加5秒
            document.getElementById("timer").innerText='视频时长：'+timeLength

		}
	}
	

	$.fn.dragslot = function(options){
		var obj = new Dragslot(this,options);
		return{
           slotContainer:obj.slotContainer,
           dragStartEvent:obj.dragStartEvent
        }
	}

})(window.jQuery, window, document);