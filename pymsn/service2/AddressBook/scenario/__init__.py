# -*- coding: utf-8 -*-
#
# Copyright (C) 2007 Johann Prieur <johann.prieur@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#

name = "scenario"
description = ""

import sync.AddressBookInitialScenario
import sync.MembershipInitialScenario

import contacts.MessengerContactAddScenario
import contacts.MailContactAddScenario
import contacts.MobileContactAddScenario
import contacts.ContactDeleteScenario

import contacts.BlockContactScenario
import contacts.UnblockContactScenario

import contacts.DeclineInviteScenario
import contacts.AcceptInviteScenario
import contacts.CheckPendingInviteScenario

import groups.GroupAddScenario
import groups.GroupDeleteScenario
import groups.GroupRenameScenario
import groups.GroupContactAddScenario
import groups.GroupContactDeleteScenario
