// Transcrypt'ed from Python, 2022-09-15 13:46:24
var random = {};
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import * as __module_random__ from './random.js';
__nest__ (random, '', __module_random__);
var __name__ = '__main__';
export var gen_random_int = function (number, seed) {
	random.seed (seed);
	var array = (function () {
		var __accu0__ = [];
		for (var i = 0; i < number; i++) {
			__accu0__.append (random.randint (-(50), 50));
		}
		return __accu0__;
	}) ();
	return array;
};
export var generate = function () {
	var number = 10;
	var seed = 200;
	var array = gen_random_int (number, seed);
	var array_str = ', '.join (array) + '.';
	document.getElementById ('generate').innerHTML = array_str;
};
export var sortnumber1 = function () {
	var array_str = document.getElementById ('generate').innerHTML;
	var sortedarray = (function () {
		var __accu0__ = [];
		for (var i of array_str.strip ().py_split (',')) {
			__accu0__.append (int (i));
		}
		return __accu0__;
	}) ();
	var n = len (sortedarray);
	var swapped = true;
	while (swapped) {
		var swapped = false;
		var new_n = 0;
		for (var inner_index = 1; inner_index < n; inner_index++) {
			if (sortedarray [inner_index - 1] > sortedarray [inner_index]) {
				var __left0__ = tuple ([sortedarray [inner_index - 1], sortedarray [inner_index]]);
				sortedarray [inner_index] = __left0__ [0];
				sortedarray [inner_index - 1] = __left0__ [1];
				var swapped = true;
				var new_n = inner_index;
			}
		}
		var n = new_n;
	}
	var array_str = ', '.join (sortedarray) + '.';
	document.getElementById ('sorted').innerHTML = array_str;
};
export var sortnumber2 = function () {
	var value = document.getElementsByName ('numbers') [0].value;
	if (value == '') {
		window.alert ('Your textbox is empty');
		return ;
	}
	var sortedarray = (function () {
		var __accu0__ = [];
		for (var i of value.strip ().py_split (',')) {
			__accu0__.append (int (i));
		}
		return __accu0__;
	}) ();
	var n = len (sortedarray);
	for (var outer_index = 1; outer_index < n; outer_index++) {
		var inner_index = outer_index;
		var temp_val = sortedarray [inner_index];
		while (inner_index > 0 && temp_val < sortedarray [inner_index - 1]) {
			sortedarray [inner_index] = sortedarray [inner_index - 1];
			inner_index--;
		}
		sortedarray [inner_index] = temp_val;
	}
	var array_str = ', '.join (sortedarray) + '.';
	document.getElementById ('sorted').innerHTML = array_str;
};

//# sourceMappingURL=library.map